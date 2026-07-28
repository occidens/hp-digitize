import os

tty="/dev/cu.usbserial-FTF06UDC"

# stty -F /dev/ttyUSB0 115200 \
#   cs8 -parenb -cstopb \
#   clocal -crtscts \
#   raw -echo -echoe -echok -echoctl -echoke \
#   -ixon -ixoff -crtscts \
#   min 1 time 0

print("open...")
f=open(tty,"wb")
print("done")

# print("stty...")
# #os.system(f"stty -f {tty} 9600 raw -echo clocal")
# print("done")

print("sending...")
f.write(b"IN;SP4;")
f.flush()
f.close()
print("done")