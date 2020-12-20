from onewheel import UUIDs
from onewheel.utils import onewheel_device, unlock_gatt_sequence, as_int, riding_mode_name
from const import WHEEL_MAC

with onewheel_device(WHEEL_MAC) as device:
    unlock_gatt_sequence(device)
    mode = device.char_read(UUIDs.RidingMode)

    print(riding_mode_name(as_int(mode)))
