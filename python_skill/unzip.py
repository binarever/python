import zipfile

zFile=zipfile.ZipFile("evil.zip")

try:
	zFile.extractall(pwd="secret")
except Exception ,  e:
	print e 