import socket

print "Creating socket..."
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
print "done."

print "Connecting to remote host..."
s.connect(("www.dicnocy.cn",80))
print "done."
