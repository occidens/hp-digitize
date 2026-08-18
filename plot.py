import serial
import time
from datetime import datetime

TTY = "/dev/cu.usbserial-FTF06UDC"

plotter = serial.Serial(
    port=TTY,
    baudrate=9600,
    bytesize=serial.EIGHTBITS,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    rtscts=False, dsrdtr=False, xonxoff=False,
    timeout=1, write_timeout=10,
    exclusive=True,          # fail loudly if something else has the port
)

def write(s):
    nbytes = len(s)
    plotter.write(s.encode('ascii'))
    time.sleep(2 * nbytes / 1000)

plotter.reset_input_buffer()

def wait_for_input():
    while plotter.in_waiting == 0:
        time.sleep(0.1) # min bytes that we will get back before readline

def buf_remaining():


    plotter.write(b'\x1b.B') # send control sequence to plotter
    t0 = datetime.now()
    # # raw = plotter.read(20) # could take up to 1s
    # raw = plotter.readline(6)
    raw = plotter.read_until(b'\r')
    t1 = datetime.now()

    print(f'raw response: {raw}')

    if len(raw) > 0:
        available = int(raw.decode('ascii').strip())
    else:
        available = 0


    t = t1 - t0
    print(f'Reading back bytes took {t.microseconds}μs')
    return available

def plot(commands: list[str]):
    combytes = [ command.encode('ascii') for command in commands ]
    available = buf_remaining()

    for command in combytes:
        t0 = datetime.now()

        needed = len(command)

        while needed > available:
            time.sleep(0.1)
            available = buf_remaining()

        plotter.write(command)
        available -= needed

        t1 = datetime.now()
        t = t1 - t0
        print(f'Command took {t.microseconds}μs')

# buf_remaining() {
#   local bytes
#   printf '\x1b.b' >&3

#  Wait one sec to read from file, test if data is available and reads 6 bytes to bytes
#   ifs= read -t 1 -n6 bytes <&3

# If exit status of last command isn't 0, print offline

#   if [[ $? -ne 0 ]]; then
#     echo "offline" > data/status
#     if [[ "$last" != "offline" ]]; then
#       event status offline | publish progress &
#       last=offline
#     fi
#     event stop | publish progress &
#     exit 5

# If exit status of last command was successful then Print online

#   else
#     echo "online" > data/status
#     if [[ "$last" != "online" ]]; then
#       event status online | publish progress &
#       last=online
#     fi
#   fi

#   available="${bytes:-0}"
# }

# buf_remaining

# while ifs= read -r line; do
#   needed=${#line}
#   while [[ $needed -gt $available ]]; do
#     sleep 0.1
#     buf_remaining
#   done
#   echo -n "$line" >&3
#   ((available-=$needed))
#   echo "$line (buf: $available bytes avail.)"
# done | event_stream


