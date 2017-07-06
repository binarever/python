import urllib

body=urllib.urlopen("http://www.baidu.com")

print body.read()