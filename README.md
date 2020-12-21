# onewheel-bluetooth

Provides some python helpers for prototyping BLE applications for the Onewheel.

### Usage

The helpers in `onewheel.utils` should help you quickly get something which talks to your wheel.

You first need to find your device's MAC address and the "secret" used in unlocking the board. I did both by capturing bluetooth HCI logs from the official android app. Once you [enable HCI logs](https://fte.com/WebHelpII/Sodera/Content/Documentation/WhitePapers/BPA600/Encryption/GettingAndroidLinkKey/RetrievingHCIlog.htm) in Android, you can open the official OW app, ride your wheel for a moment, then generate an android bug report, which contains the bluetooth logs.

If you look in the logs for a `Write Request` for `UUIDs.UartSerialWrite`, the value logged is the "secret" to supply to this project's unlock sequence.

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
