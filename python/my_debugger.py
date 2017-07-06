from ctypes import *
from my_debugger_defines import *

Kernel32=windll.Kernel32

class debugger():
	def __init__(self):
		self.h_process=None
		self.pid=None
		self.debugger_active=False
		self.h_thread=None
		self.context=None
		self.exception=None
		self.exception_address=None
		self.breakpoints={}
		self.first_breakpoint=True
		self.hardware_breakpoints={}
		
		system_info=SYSTEM_INFO()
		Kernel32.GetSystemInfo(byref(system_info))
		self.page_size=system_info.dwPageSize
		
		self.guard_pages=[]
		self.memory_breakpoints={}
		
	def load(self,path_to_exe):
		
		creation_flags=DEBUG_PROCESS
		
		startupinfo=STARTUPINFO()
		process_information=PROCESS_INFORMATION()
		
		startupinfo.dwFlags=0x1
		startupinfo.wShowWindow=0x0
		
		startupinfo.cb=sizeof(startupinfo)
		
		if Kernel32.CreateProcessA(path_to_exe,None,None,None,None,creation_flags,None,None,byref(startupinfo),byref(process_information)):
			print "[*]We have successfully launched the process!"
			print "[*]PID:%d"%process_information.dwProcessId
			self.h_process=self.open_process(process_information.dwProcessId)
			
		else:
			print "[*]Error:0x%08x."%Kernel32.GetLastError()
			
	def open_process(self,pid):
		
		self.h_process=Kernel32.OpenProcess(PROCESS_ALL_ACCESS,False,pid)
		return self.h_process
		
	def attach(self,pid):
		
		self.h_process=self.open_process(pid)
		
		if Kernel32.DebugActiveProcess(pid):
			self.debugger_active=True
			self.pid=int(pid)
			#self.run()
		
		else:
			print "[*]Unable to attach to the process."
			
	def run(self):
		
		while self.debugger_active==True:
			self.get_debug_event()
			
	def get_debug_event(self):
		
		debug_event=DEBUG_EVENT()
		continue_status=DBG_CONTINUE
		
		if Kernel32.WaitForDebugEvent(byref(debug_event),INFINITE):
			#raw_input("press a key to continue...")
			#self.debugger_active=False
			
			self.h_thread=self.open_thread(debug_event.dwThreadId)
			self.context=self.get_thread_context(self.h_thread)
			
			print "Event Code:%d Thread ID:%d"%(debug_event.dwDebugEventCode,debug_event.dwThreadId)
			
			if debug_event.dwDebugEventCode==EXCEPTION_DEBUG_EVENT:
				self.exception=debug_event.u.Exception.ExceptionRecord.ExceptionCode
				self.exception_address=debug_event.u.Exception.ExceptionRecord.ExceptionAddress
				
			if self.exception==EXCEPTION_ACCESS_VIOLATION:
				print "Access Violation Detected."
			elif self.exception==EXCEPTION_BREAKPOINT:
				continue_status=self.exception_handler_breakpoint()
			elif self.exception==EXCEPTION_GUARD_PAGE:
				print "Guard Page Access Detected."
			elif self.exception==EXCEPTION_SINGLE_STEP:
				#print "Single Stepping."
				self.exception_handler_single_step()
				
			Kernel32.ContinueDebugEvent(debug_event.dwProcessId,debug_event.dwThreadId,continue_status)
			
	def exception_handler_breakpoint(self):
		
		print "[*]Inside the breakpoint handler."
		print "Exception address:0x%08x"%self.exception_address
		return DBG_CONTINUE
		
	def exception_handler_single_step(self):
		
		if self.context.Dr6&0x1 and self.hardware_breakpoints.has_key(0):
			slot=0
		elif self.context.Dr6&0x2 and self.hardware_breakpoints.has_key(1):
			slot=1
		elif self.context.Dr6&0x4 and self.hardware_breakpoints.has_key(2):
			slot=2
		elif self.context.Dr6&0x8 and self.hardware_breakpoints.has_key(3):
			slot=3
		else:
			continue_status=DBG_EXCEPTION_NOT_HANDLED
			
		if self.bp_del_hw(slot):
			continue_status=DBG_CONTINUE
			
		print "[*]Hardware breakpoint removed."
		return continue_status
		
	def detach(self):
		
		if Kernel32.DebugActiveProcessStop(self.pid):
			print "[*]Finished debugging.Exiting..."
			return True
		else:
			print "There was an error"
			return False
			
	def open_thread(self,thread_id):
		
		h_thread=Kernel32.OpenThread(THREAD_ALL_ACCESS,None,thread_id)
		
		if h_thread is not None:
			return h_thread
			
		else:
			print "[*]Could not obtain a valid thread handle."
			return False
			
	def enumerate_threads(self):
		
		thread_entry=THREADENTRY32()
		thread_list=[]
		snapshot=Kernel32.CreateToolhelp32Snapshot(TH32CS_SNAPTHREAD,self.pid)
		
		if snapshot is not None:
			
			thread_entry.dwSize=sizeof(thread_entry)
			success=Kernel32.Thread32First(snapshot,byref(thread_entry))
			print thread_entry.th32OwnerProcessID
			print self.pid
			
			while success:
				if thread_entry.th32OwnerProcessID==self.pid:
					thread_list.append(thread_entry.th32ThreadID)
				success=Kernel32.Thread32Next(snapshot,byref(thread_entry))
				
			Kernel32.CloseHandle(snapshot)
			return thread_list
					
		else:
			print "enumerate_threads fail."
			return False
					
	def get_thread_context(self,thread_id):
		
		context=CONTEXT()
		context.ContextFlags=CONTEXT_FULL|CONTEXT_DEBUG_REGISTERS
		
		h_thread=self.open_thread(thread_id)
		if Kernel32.GetThreadContext(h_thread,byref(context)):
			return context
			
		else:
			print "get_thread_context fail."
			return False
			
	def read_process_memory(self,address,length):
		data=""
		read_buf=create_string_buffer(length)
		count=c_ulong(0)
		
		if not Kernel32.ReadProcessMemory(self.h_process,address,read_buf,length,byref(count)):
			
			return False
			
		else:
			data+=read_buf.raw
			return data
			
	def write_process_memory(self,address,data):
		
		count=c_ulong(0)
		length=len(data)
		
		c_data=c_char_p(data[count.value:])
		
		if not Kernel32.WriteProcessMemory(self.h_process,address,c_data,length,byref(count)):
			return False
			
		else:
			return True
			
	def bp_set(self,address):
		
		if not self.breakpoints.has_key(address):
			try:
				original_byte=self.read_process_memory(address,1)
				
				print "original_byte:".original_byte
				
				res=self.write_process_memory(address,"\xCC")
				
				print res  
				if res is not None:  
					print "write sucessful"
				else:
					print "write fail"
				
				self.breakpoints[address]=(address,original_byte)
				
			except:
				return False
				
		return True
		
	def bp_set_hw(self,address,length,condition):
		
		if length not in (1,2,4):
			return False
		else:
			length-=1
			
		if condition not in (HW_ACCESS,HW_EXECUTE,HW_WRITE):
			return False
		
		if not self.hardware_breakpoints.has_key(0):
			available=0
		elif not self.hardware_breakpoints.has_key(1):
			available=1
		elif not self.hardware_breakpoints.has_key(2):
			available=2
		elif not self.hardware_breakpoints.has_key(3):
			available=3
		else:
			return False
			
		for thread_id in self.enumerate_threads():
			context=self.get_thread_context(thread_id=thread_id)
			
			context.Dr7|=1<<(available*2)
			
			if available==0:
				self.context.Dr0=address
			elif available==1:
				self.context.Dr1=address
			elif available==2:
				self.context.Dr2=address
			elif available==3:
				self.context.Dr3=address
			
			context.Dr7|=condition<<((available*4)+16)
		
			context.Dr7|=length<<((available*4)+18)
		
			h_thread=self.open_thread(thread_id)
			Kernel32.SetThreadContext(h_thread,byref(context))
		
		self.hardware_breakpoints[available]=(address,length,condition)
		
		return True
		
	def bp_del_hw(self,slot):
		
		for thread_id in self.enumerate_threads():
			
			context=self.get_thread_context(thread_id=thread_id)
			
			context.Dr7&=~(1<<(slot*2))
			
			if slot==0:
				context.Dr0=0x00000000
			elif slot==1:
				context.Dr1=0x00000000
			elif slot==2:
				context.Dr2=0x00000000
			elif slot==3:
				context.Dr3=0x00000000
				
			context.Dr7&=~(3<<((slot*4)+16))
			
			context.Dr7&=~(3<<((slot*4)+18))
			
			h_thread=self.open_thread(thread_id)
			Kernel32.SetThreadContext(h_thread,byref(context))
			
		del hardware_breakpoints[slot]
			
		return True
		
	def bp_set_mem(self,address,size):
		
		mbi=MEMORY_BASIC_INFORMATION()
		
		if Kernel32.VirtualQueryEx(self.h_process,address,byref(mbi),sizeof(mbi))<sizeof(mbi):
			return False
			
		current_page=mbi.BaseAddress
		
		while current_page<=address+size:
			
			self.guard_pages.append(current_page)
			
			old_protection=c_ulong(0)
			if not Kernel32.VirtualProtectEx(self.h_process,current_page,size,mbi.Protect|PAGE_GUARD,byref(old_protection)):
				return False
				
			current_page+=self.page_size
			
		self.memory_breakpoints[address]=(address,size,mbi)
		
		return True
		
	def func_resolve(self,dll,function):
		
		handle=Kernel32.GetModuleHandleA(dll)
		address=Kernel32.GetProcAddress(handle,function)
		
		Kernel32.CloseHandle(handle)
		
		return address