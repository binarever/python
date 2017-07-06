from sulley import *

s_initialize("War-FTP")
s_group("verbs",values=["USER","PASSWORD"])
if s_block_start("body",group = "verbs"):

	s_delim(" ")
	s_string("A"*1000)
	s_static("\r")
s_block_end()