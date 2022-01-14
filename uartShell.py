import os, sys, serial, time

BAUD_RATE = 115200

if os.geteuid() != 0:
    print("[x] Please, run %s as root" % sys.argv[0])
    exit()

if len(sys.argv) != 2:
    print("[x] Usage: %s <usb port>" % sys.argv[0])
    exit()

s = serial.Serial(sys.argv[1], BAUD_RATE)

# Stop U-Boot sequence
while "SigmaStar #" not in s.readline().decode("utf-8", errors="ignore"):
    s.write("\r\n".encode("utf-8"))

print("[+] Got U-Boot shell")
print("[+] Getting /bin/sh shell...")

# Set a timeout and read everything in the input buffer (s.reset_input_buffer() won't work since USB adapter has its own buffer)
s.timeout = 1
while "SigmaStar #" in s.readline().decode("utf-8", errors="ignore"): pass
s.timeout = None

s.write("setenv bootargs console=ttyS0,115200 root=/dev/mtdblock2 rootfstype=squashfs ro init=/bin/sh LX_MEM=0x3fe0000 mma_heap=mma_heap_name0,miu=0,sz=0x1400000 mma_memblock_remove=1\r\n".encode("utf-8"))
s.write("run bootcmd\r\n".encode("utf-8"))

s.read_until("/bin/sh: can't access tty; job control turned off".encode("utf-8"))

print("[+] Got /bin/sh shell")
print("[+] Setting up linux...")

s.write("./linuxrc &\r\n".encode("utf-8"))

time.sleep(10)

s.timeout = 1
while s.readline().decode("utf-8", errors="ignore"): pass
s.timeout = None

print("[+] Ready")

os.system("screen %s %d" % (sys.argv[1], BAUD_RATE))
