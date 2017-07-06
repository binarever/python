import hashlib

def deal1(line):
	aline=hashlib.md5(line).hexdigest()
	print aline
	f=open('md5.txt','a+')
	f.write(aline+"\n")
	f.close()

def deal2(line):
	aline=hashlib.sha1(line).hexdigest()
	print aline
	f=open('sha1.txt','a+')
	f.write(aline+"\n")
	f.close()

def deal3(line):
	aline=hashlib.sha224(line).hexdigest()
	print aline
	f=open('sha224.txt','a+')
	f.write(aline+"\n")
	f.close()

def deal4(line):
	aline=hashlib.sha256(line).hexdigest()
	print aline
	f=open('sha256.txt','a+')
	f.write(aline+"\n")
	f.close()

def deal5(line):
	aline=hashlib.sha384(line).hexdigest()
	print aline
	f=open('sha384.txt','a+')
	f.write(aline+"\n")
	f.close()

def deal6(line):
	aline=hashlib.sha512(line).hexdigest()
	print aline
	f=open('sha512.txt','a+')
	f.write(aline+"\n")
	f.close()

def main():
	file=open('rockyou.txt')
	for line in file.readlines():
		print line
		deal1(line)
		deal2(line)
		deal3(line)
		deal4(line)
		deal5(line)
		deal6(line)
	file.close()

if __name__=='__main__':
	main()