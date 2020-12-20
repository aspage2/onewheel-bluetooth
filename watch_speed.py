import multiprocessing
from binascii import hexlify
from time import sleep

from const import WHEEL_MAC
from onewheel import UUIDs
from plotter import plotter_main

from onewheel.utils import unlock_gatt_sequence, onewheel_device
from functools import partial

plots = {
    UUIDs.SpeedRpm: {
        "title": "Speed (rpm)",
    },
    UUIDs.TiltAngleRoll: {
        "title": "Roll angle",
    },
    UUIDs.Odometer: {
        "title": "Odometer",
    },
    UUIDs.BatteryRemaining: {
        "title": "Battery Remaining",
    }
}


def main(value_cb, pts):
    with onewheel_device(WHEEL_MAC) as device:
        print("unlocking")
        unlock_gatt_sequence(device)
        device.char_write(UUIDs.SpeedRpm, b'\0')

        for uuid in pts:
            def handle(u, _, data):
                val = int(hexlify(data), base=16)
                value_cb((u, val))
            device.subscribe(uuid, partial(handle, uuid))

        while True:
            device.char_write(UUIDs.SpeedRpm, b'\0')
            sleep(10)


if __name__ == "__main__":
    q = multiprocessing.Queue()
    try:
        multiprocessing.Process(target=plotter_main, args=(q.get, plots)).start()
        main(q.put, plots)
    finally:
        q.close()
