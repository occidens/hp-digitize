import os
import serial
import time

SQUARE = "IN;SP4;PA90,90;PD;PA90,900;PA900,900;PA900,90;PA90,90;PU;SP0;"
INIT = "IN;SP4;OA;"
CLOSE = "IN;SP0;"

# baud rate: 9600, data bits: 8, flow control: none, parity: none, stop bits: 1
# stty -f /dev/tty.usbserial 9600 cs8 -cstopb -parenb

# pip install pyserial

tty = "/dev/cu.usbserial-FTF06UDC"

plotter = serial.Serial(
    port="/dev/cu.usbserial-FTF06UDC",
    baudrate=9600,
    bytesize=serial.EIGHTBITS,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    rtscts=False, dsrdtr=False, xonxoff=False,
    timeout=2, write_timeout=10,
    exclusive=True,          # fail loudly if something else has the port
)

time.sleep(2)                # let DTR/RTS settle
plotter.reset_input_buffer()

# plotter.write(b"\x1b.B")     # same handshake your Linux script uses
# print("buffer reply:", plotter.read(10))

plotter.write(INIT.encode("ascii"))





plotter.readline()
# plotter.flush()
# time.sleep(2)                # let the FIFO actually drain
plotter.close()

# try:
#     plotter = serial.Serial(
#         port=tty,
#         baudrate=9600,
#         bytesize=serial.EIGHTBITS,
#         parity=serial.PARITY_NONE,
#         stopbits=serial.STOPBITS_ONE
#     )
# except serial.SerialException as e:
#     print(f"Error opening serial port: {e}")
#     exit()
# try:
#     plotter.write(SQUARE.encode('ascii'))
#     plotter.flush()
#     print('Successfully flushed')
# except Exception as e:
#     print(f"Error running plotter command: {e}")

# finally:
#     plotter.close()
#     print("Connection closed.")