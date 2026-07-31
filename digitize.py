import signal
import serial
import time
import sys
import turtle as t

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

time.sleep(1)                # let DTR/RTS settle
plotter.reset_input_buffer()



result = []

def finish(signum, frame):
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    print(f'Got signal {signum}')
    print(result)
    plot()
    # sys.exit(0)

handler = signal.signal(signal.SIGINT, finish)

def write(s):
    nbytes = len(s)
    plotter.write(s.encode('ascii'))
    time.sleep(2 * nbytes / 1000)
    # time.sleep(1)

def wait_for_input():
    while plotter.in_waiting == 0:
        time.sleep(0.1) # min bytes that we will get back before readline

def plot():
    t.setup(800,600)
    t.screensize(10300 / 10, 7650 / 10)
    for (x, y, p) in result:
        if p == 0:
            t.penup()
        else:
            t.pendown()
        t.setpos(x / 10, y / 10)

write('IN;SP4;')

while True:
    write('DP;')
    print('Enter point')
    while True:
        write('OS;')
        wait_for_input()
        raw_status = plotter.readline()
        if raw_status == b'':
            continue
        status = int(raw_status)
        print(f'status: {status}')
        if (status & 4):
            break
    write('OD;')
    wait_for_input()
    raw_output = plotter.readline().decode('ascii')
    print(f'Raw output: {raw_output}')
    x,y,p = map(int,raw_output.split(','))
    result.append((x,y,p))
    print(f'Recorded point {x},{y} with pen status {p}')

# 0000
#

# plotter.write(b"\x1b.B")     # same handshake your Linux script uses
# print("buffer reply:", plotter.read(10))
