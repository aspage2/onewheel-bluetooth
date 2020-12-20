
from onewheel import UUIDs
from onewheel.utils import onewheel_device, unlock_gatt_sequence
from const import WHEEL_MAC

with onewheel_device(WHEEL_MAC) as dev:
    unlock_gatt_sequence(dev)

    print(dev.char_write(UUIDs.RidingMode, bytes.fromhex("0004")))

