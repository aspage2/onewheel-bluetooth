
# Onewheel notes

read 0x001d (riding mode), returns 0000

read hardware version, my wheel returns 1074
read firmware version, my wheel returns 1036

turn OFF notifications for UART-read characteristic

turn ON notifications for ridingmode characteristic (handle 0x001d value, 0x001e CCCD)
turn ON notifications for lighting mode characteristic (handle 0x0045 value, 0x0046 CCCD)

write secret password to UART-write characteristic: 

wait for ridingmode and lightingmode characteristics to return a notification

write 00 to the speed characteristic (0x0041) every 10 seconds

turn on notifs for a shitload of characteristics

