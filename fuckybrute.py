import win32con
import win32file
import exrex

# This needs to be ran in 32 bit python 

FuckyHandle = win32file.CreateFile(
	"\\\\.\\PhysicalDrive4", # Change this according to: wmic diskdrive list brief
	0xC0000000, 
	win32con.FILE_SHARE_READ | win32con.FILE_SHARE_WRITE, 
	None, 
	win32con.OPEN_EXISTING, 
	0, 
	0
)

OutBuffer = bytearray(b"\x00"*80)

CHARSET = r"[a-zA-Z0-9]{6}" 
Combinations = exrex.count(CHARSET)

for N, Password in enumerate(exrex.generate(CHARSET)):

	InBuffer = (
		b"\x2c\x00\x00\x00\x00\x00\x10\x18\x00\x00\x00\x00\x20\x00\x00\x00\x0A\x00\x00\x00\x50\x00\x00\x00\x30\x00\x00\x00\xf4\x01" + 
		b"\x00" * 50 + 
		Password.encode("ascii") + 
		b"\x00" * 60
	)
	
	try:
		win32file.DeviceIoControl(FuckyHandle, 0x4D004, InBuffer, OutBuffer)
	except Exception as Error:
		print(Error)
		print()

	Unlocked = OutBuffer[2] == 0

	if N % 100 == 0:
		print(Password, f'{round(N/Combinations*100,7):.6f}%', end="\r")

	if Unlocked:
		print("="*40)
		print(Password)
		break