import socket
import os
import struct
from ctypes import*

host  =  "192.168.1.104"

class  IP(Structure):
	_field_  =  [
	("ihl",c_ubyte,4),
	("version",c_ubyte,4),
	("tos",c_ubyte),
	("len",c_ushort),
	("id",c_ushort),
	("offset",c_ushort),
	("ttl",c_ubyte),
	("protocol_num",c_ubyte),
	("sum",c_ushort),
	("src",c_ulong),
	("dst",c_ulong)
	]

class ICMP(Structure):
	_field_   =   [
	("type",c_ubyte),
	("code",c_ubyte),
	("checksum",c_ushort),
	("unused",c_ushort),
	("next_hop_mtu",c_ushort)
	]

def _new_(self,socket_buffer=None):
	return self.from_buffer_copy(socket_buffer)

def _init_(self,socket_buffer=None):
	pass

if os.name=="nt":
	socket_protocol  =  socket.IPPROTO_IP
else:
	socket_protocol  =  socket.IPPROTO_ICMP

sniffer  =  socket.socket(socket.AF_INET,socket.SOCK_RAW,socket_protocol)

sniffer.bind((host,0))
sniffer.setsockopt(socket.IPPROTO_IP,socket.IP_HDRINCL,1)

if os.name=="nt":
	sniffer.ioctl(socket.SIO_RCVALL,socket.RCVALL_ON)

try :
	while True:
		raw_buffer  =  sniffer.recvfrom(65565)[0]

		ip_header  =  IP(raw_buffer[0:20])

		print "Protocol :  %s  %s ->  %s "  % (ip_header.protocol,ip_header.src_address,ip_header.dst_address)

		if ip_header.protocol=="ICMP":
			offset  =  ip_header.ihl*4
			huf  =  raw_buffer[offset:offset+sizeof(ICMP)]

			icmp_header  =  ICMP(buf)

			print "ICMP->  Type :  %d  Code:  %d"  %   (icmp_header.type,icmp_header.code)

except KeyboardInterrupt:

	if os.name=="nt":
		sniffer.ioctl(socket.SIO_RCVALL,socket.RCVALL_OFF)