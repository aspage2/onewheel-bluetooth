import logging

from binascii import hexlify
from contextlib import contextmanager
from time import sleep

from pygatt import GATTToolBackend, BLEAddressType, exceptions

from onewheel import UUIDs

_util_logger = logging.getLogger("onewheel-util")
_util_logger.setLevel(logging.INFO)


def riding_mode_name(code: int) -> str:
    """String name for current riding mode.

    Raises an IndexOutOfBounds error if the code isn't in the
    inclusive range [4, 9]
    """
    return [
        "Sequoia",
        "Cruz",
        "Mission",
        "Elevated",
        "Delirium",
        "Custom",
    ][code - 4]


def as_int(char_data: bytes) -> int:
    """Convert the bytestring into an integer"""
    return int(hexlify(char_data), base=16)


def unlock_gatt_sequence(device, secret):
    """Unlocks the onewheel device.

    This should be called first and only once. To keep the connection open,
    Write a single zero-byte to the SpeedRpm characteristic every 10-20 seconds.

    The unlock sequence won't occur if the subroutine determines that the
    device is already unlocked.
    """
    data = device.char_read(UUIDs.RidingMode)
    if data != b'\0\0':
        _util_logger.info("Device already unlocked")
        return
    device.char_read(UUIDs.HardwareRevision)
    device.char_read(UUIDs.FirmwareRevision)
    device.unsubscribe(UUIDs.UartSerialRead)

    riding_mode = None
    lighting_mode = None

    def handle_riding_mode(_, data):
        nonlocal riding_mode
        _util_logger.info(f"RidingMode received: {int(hexlify(data), base=16)}")
        riding_mode = data

    def handle_lighting_mode(_, data):
        nonlocal lighting_mode
        _util_logger.info(f"lightingMOde received: {int(hexlify(data), base=16)}")
        lighting_mode = data

    device.subscribe(UUIDs.RidingMode, handle_riding_mode)
    device.subscribe(UUIDs.LightingMode, handle_lighting_mode)
    device.char_write(UUIDs.UartSerialWrite, bytearray.fromhex(secret))
    _util_logger.debug("Waiting for riding & lighting modes to return values")
    while lighting_mode is None and riding_mode is None:
        sleep(0.25)


@contextmanager
def onewheel_device(mac):
    """Open a pygatt device using the GATTool backend.

    on __exit__, cleans up the device and backend.
    """
    adapter = GATTToolBackend()
    adapter.start()
    device = adapter.connect(mac, address_type=BLEAddressType.public)
    try:
        yield device
    except exceptions.NotificationTimeout:
        print("Timed out.")
    finally:
        device.disconnect()
        adapter.stop()
