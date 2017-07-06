from immlib import *

def main(args):
	
	imm=Debugger()
	
	bad_char_found=False
	
	address=int(args[0],16)
	
	shellcode="\x33\xDB\x53\x68\x48\x41\x43"
	"\x4B\x8B\xC4\x53\x50\x50\x53\xB8\xEA"
	"\x07\xD5\x77\xFF\xD0\x33\xC0\x50\xB8\xFA\xCA\x81\x7C\xFF\xD0"
	shellcode_length=len(shellcode)
	
	debug_shellcode=imm.readMemory(address,shellcode_length)
	debug_shellcode=debug_shellcode.encode("HEX")
	
	imm.log("Address:0x%08x"%address)
	imm.log("Shellcode Length:%d"%shellcode_length)
	
	imm.log("Attack Shellcode:%s"%shellcode[:shellcode_length])
	imm.log("In Memory Shellcode:%s"%debug_shellcode[:shellcode_length])
	
	count=0
	while count<=shellcode_length:
		
		if debug_shellcode[count]!=shellcode[count]:
			
			imm.log("Bad Char Detected at offset %d"%count)
			bad_char_found=True
			break
			
		count+=1
		
	if bad_char_found:
		imm.log("[*****]")
		imm.log("Bad character found:%s"%debug_shellcode[count])
		imm.log("Bad character original:%s"%shellcode[count])
		imm.log("[*****]")
		
	return "[*]!badchar finished,check Log window."