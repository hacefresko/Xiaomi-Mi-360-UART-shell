# Xiaomi Mi 360 UART shell

Python script to get a `/bin/sh` shell on Xiaomi Mi 360 Home Security Camera 2K via UART serial port. It has only be tested on model `MJSXJ09CM`.

It interrupts the U-Boot boot sequence to get an U-Boot shell and modify the bootargs to execute `/bin/sh` instead of `linuxrc`, which is the script that configures the camera. When the shell is ready, it executes `linuxrc` in the background so that the camera can be used as usual while the shell is still active.

Here is a photo of the UART port in the camera:

![UART port in model MJSXJ09CM](https://raw.githubusercontent.com/hacefresko/Xiaomi-Mi-360-UART-shell/master/UART.jpeg)
