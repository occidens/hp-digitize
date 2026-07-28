import os
import serial

SQUARE = "IN;SP4;PA90,90;PD;PA90,900;PA900,900;PA900,90;PA90,90;PU;SP0;"

# baud rate: 9600, data bits: 8, flow control: none, parity: none, stop bits: 1
# stty -f /dev/tty.usbserial 9600 cs8 -cstopb -parenb

# pip install pyserial

tty = "/dev/tty.usbserial-FTF06UDC"


try:
    plotter = serial.Serial(
        port=tty,
        baudrate=9600,
        bytesize=serial.EIGHTBITS,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE
    )
except serial.SerialException as e:
    print(f"Error opening serial port: {e}")
    exit()
try:
    plotter.write(SQUARE.encode('ascii'))
    plotter.flush()
    print('Successfully flushed')
except Exception as e:
    print(f"Error running plotter command: {e}")

finally:
    plotter.close()
    print("Connection closed.")