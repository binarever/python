import sys
from ctypes import *

PAGE_READWRITE=0x04
PROCESS_ALL_ACCESS=(0x000F0000|0x00100000|0xFFF)
VIRTUAL_MEM=(0x1000|0x2000)

Kernel32=windll.Kernel32
pid=sys.argv[1]
dll_path=sys.argv[2]
dll_len=len(dll_path)

h_process=Kernel32.OpenProcess(PROCESS_ALL_ACCESS,False,int(pid))

if not h_process:
	print "[*]Couldn't acquire a handle to PID:%s"%pid
	sys.exit(0)
	
arg_address=Kernel32.VirtualAllocEx(h_process,0,dll_len,VIRTUAL_MEM,PAGE_READWRITE)

written=c_int(0)
Kernel32.WriteProcessMemory(h_process,arg_address,dll_path,dll_len,byref(written))

h_Kernel32=Kernel32.GetModuleHandleA("Kernel32.dll")
h_loadlib=Kernel32.GetProcAddress(h_Kernel32,"LoadLibraryA")

thread_id=c_ulong(0)

if not Kernel32.CreateRemoteThread(h_process,None,0,h_loadlib,arg_address,0,byref(thread_id)):
	
	print "[*] Failed to inject the DLL.Exiting."
	sys.exit(0)
	
print "[*] Remote thread with ID 0x%08x created"%thread_id.value