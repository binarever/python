import socket,traceback

host=''
port=51423

s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
s.bind((host,port))
s.listen(1)

while 1:
	try:
		clientsock,clientaddr=s.accept()
	except KeyboardInterrupt:
		raise
	except:
		traceback.print_exc()
		cotinue

	try:
		print "Got connection from",clientsock.getpeername()
	except (KeyboardInterrupt,SystemExit):
		traceback.print_exc()

	try:
		clientsock.close()
	except KeyboardInterrupt:
		raise
	except:
		traceback.print_exc()
