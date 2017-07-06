from ctypes import *

WORD=c_ushort
DWORD=c_ulong
LPBYTE=POINTER(c_ubyte)
LPTSTR=POINTER(c_char)
HANDLE=c_void_p
PVOID = c_void_p
ULONG_PTR = POINTER(c_ulong)
LPVOID    = c_void_p
UINT_PTR  = c_ulong
SIZE_T    = c_ulong
DWORD64 = c_uint64
LONG=c_long
ULONG=c_ulong
UCHAR=c_ubyte

DEBUG_PROCESS=0x00000001
CREATE_NEW_CONSOLE=0x00000010
PROCESS_ALL_ACCESS = 0x001F0FFF
INFINITE = 0xFFFFFFFF
DBG_CONTINUE = 0X00010002
TH32CS_SNAPTHREAD   = 0x00000004
CONTEXT_FULL = 0x00010007
CONTEXT_DEBUG_REGISTERS = 0x00010010
THREAD_ALL_ACCESS=2032639

EXCEPTION_DEBUG_EVENT = 0x1  
CREATE_THREAD_DEBUG_EVENT =0x2  
CREATE_PROCESS_DEBUG_EVENT = 0x3  
EXIT_THREAD_DEBUG_EVENT = 0x4  
EXIT_PROCESS_DEBUG_EVENT = 0x5  
LOAD_DLL_DEBUG_EVENT = 0x6  
UNLOAD_DLL_DEBUG_EVENT = 0x7  
OUPUT_DEBUG_STRING_EVENT =0x8  
RIP_EVENT = 0x9 

EXCEPTION_ACCESS_VIOLATION =0x00000005  
EXCEPTION_BREAKPOINT = 0x80000003  
EXCEPTION_GUARD_PAGE = 0x80000001  
EXCEPTION_SINGLE_STEP = 0x80000004

HW_ACCESS =0x00000003  
HW_EXECUTE =0x00000000
HW_WRITE =0x00000001

PAGE_NOACCESS                  = 0x00000001
PAGE_READONLY                  = 0x00000002
PAGE_READWRITE                 = 0x00000004
PAGE_WRITECOPY                 = 0x00000008
PAGE_EXECUTE                   = 0x00000010
PAGE_EXECUTE_READ              = 0x00000020
PAGE_EXECUTE_READWRITE         = 0x00000040
PAGE_EXECUTE_WRITECOPY         = 0x00000080
PAGE_GUARD                     = 0x00000100
PAGE_NOCACHE                   = 0x00000200
PAGE_WRITECOMBINE              = 0x00000400

class EXCEPTION_RECORD(Structure):
	pass
EXCEPTION_RECORD._fields_ = [
		("ExceptionCode",        DWORD),
		("ExceptionFlags",       DWORD),
		("ExceptionRecord",      POINTER(EXCEPTION_RECORD)),
		("ExceptionAddress",     PVOID),
		("NumberParameters",     DWORD),
		("ExceptionInformation", UINT_PTR * 15),
    ]
	
class EXCEPTION_DEBUG_INFO(Structure):
    _fields_ = [
        ("ExceptionRecord", EXCEPTION_RECORD),
		("dwFirstChance", DWORD)
	]

class _DEBUG_EVENT_UNION(Union):
    _fields_ = [
		("Exception", EXCEPTION_DEBUG_INFO),
    ]	

class DEBUG_EVENT(Structure):
    _fields_ = [
        ("dwDebugEventCode", DWORD),
        ("dwProcessId", DWORD),
        ("dwThreadId", DWORD),
        ("u", _DEBUG_EVENT_UNION)
	]

class STARTUPINFO(Structure):
	_fields_=[
		("cb",DWORD),
		("lpReserved",LPTSTR),
		("lpDesktop",LPTSTR),
		("lpTitle",LPTSTR),
		("dwX",DWORD),
		("dwY",DWORD),
		("dwXSize",DWORD),
		("dwYSize",DWORD),
		("dwXCountChars",DWORD),
		("dwYCountChars",DWORD),
		("dwFillAttribute",DWORD),
		("dwFlags",DWORD),
		("wShowWindow",WORD),
		("cbReserved2",WORD),
		("lpReserved2",WORD),
		("hStdInput",HANDLE),
		("hStdOutput",HANDLE),
		("hStdError",HANDLE),
	]
	
class PROCESS_INFORMATION(Structure):
	_fields_=[
		("hProcess",HANDLE),
		("hThread",HANDLE),
		("dwProcessId",DWORD),
		("dwThreadId",DWORD),
	]
	
class THREADENTRY32(Structure):
	_fields_=[
		("dwSize",DWORD),
		("cntUsage",DWORD),
		("th32ThreadID",DWORD),
		("th32OwnerProcessID",DWORD),
		("tpBasePri",LONG),
		("tpDeltaPri",LONG),
		("dwFlags",DWORD),
	]
	
class FLOAT_SAVE_AREA(Structure):
	_fields_=[
		("ControlWord",ULONG),
		("StatusWord",ULONG),
		("TagWord",ULONG),
		("ErrorOffset",ULONG),
		("ErrorSelector",ULONG),
		("DataOffset",ULONG),
		("DataSelector",ULONG),
		("RegisterArea",UCHAR*80),
		("Cr0NpxState",ULONG),
	]

class CONTEXT(Structure):
	_fields_=[
		("ContextFlags",DWORD),
		("Dr0",DWORD),
		("Dr1",DWORD),
		("Dr2",DWORD),
		("Dr3",DWORD),
		("Dr4",DWORD),
		("Dr5",DWORD),
		("Dr6",DWORD),
		("Dr7",DWORD),
		("FloatSave",FLOAT_SAVE_AREA),
		("SegGs",DWORD),
		("SegFs",DWORD),
		("SegEs",DWORD),
		("SegDs",DWORD),
		("Edi",DWORD),
		("Esi",DWORD),
		("Ebx",DWORD),
		("Edx",DWORD),
		("Ecx",DWORD),
		("Eax",DWORD),
		("Ebp",DWORD),
		("Eip",DWORD),
		("SegCs",DWORD),
		("EFlags",DWORD),
		("Esp",DWORD),
		("SegSs",DWORD),
	]
	
class MEMORY_BASIC_INFORMATION(Structure):
	_fields_=[
		("BaseAddress", PVOID),
		("AllocationBase", PVOID),
		("AllocationProtect", DWORD),
		("RegionSize", SIZE_T),
		("State", DWORD),
		("Protect", DWORD),
		("Type", DWORD),
	]