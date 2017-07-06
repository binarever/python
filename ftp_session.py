from sulley import *
from requests import FTP

def bind(target):
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect(target)
	s.send("USER anonymous\n")
	s.recv(buff,100)
	s.send("anonymous\n")

def do_fuzz():
	sess   = sessions.session(session_filename ="tmp.log")
	target = sessions.target("192.168.169.130",21)

    #procmon used
	target.procmon = pedrpc.client("192.168.169.130",26002)

	target.procmon_options ={
								"proc_name":"war-ftpd.exe"
							}
	sess.add_target(target)
	sess.connect(s_get("War-FTP"))
	sess.fuzz()

	print "done fuzzing..."

if 1:
	do_fuzz()