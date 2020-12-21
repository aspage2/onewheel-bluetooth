# onewheel-bluetooth

Provides some python helpers for prototyping BLE applications.

### Unlocking

The unlock sequence is implemented in `onewheel.utils.unlock_gatt_sequence`.
The routine mimics what I found from sniffing bluetooth logs from the official android
app.
This method was only tested on my particular wheel: 
`OW+ XR, Hardware: 4212, Firmware: Gemini 4153`

 * App reads `UUIDs.RidingMode`, a 0 value indicates the firmware is locked.
 * App unsubscribes from `UUIDs.UartSerialRead`
 * App subscribes to `UUIDs.RidingMode` and `UUIDs.LightingMode` characteristics.
 * App writes a secret to `UUIDs.UartSerialWrite`.
 * Wait for `RidingMode` and `LightingMode` characteristics to push their values
   via notification.

Once the device is unlocked, it can be kept unlocked by periodically sending one
zero-byte to `UUIDs.SpeedRpm`.

### Credits
UUID list and ble connection forked from https://github.com/kariudo/onewheel-bluetooth.

Thanks to [@beeradmoore](https://github.com/beeradmoore) for figuring out the md5 chunks for the serial stream reasponse via the ponewheel issue: https://github.com/ponewheel/android-ponewheel/issues/86#issuecomment-440809066
