import socket,sys
port=51423
host='localhost'

data="x"*10485760

s.socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect((host,port))

byteswritten=0
while byteswritten<len(data):
	startpos=byteswritten
	endpos=min(byteswritten+1024,len(data))
	byteswritten+=s.send(data[startpos:endpos])
	sys.stdout.write("Wrote %d bytes\r"%bytewritten)
	sys.stdout.flush()

s.shutdown(1)

print "All data sent."
while 1:
	buf=s.recv(1024)
	if not len(buf):
		break
	sys.stdout.write(buf)
