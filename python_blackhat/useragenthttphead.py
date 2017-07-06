import urllib2

url="http://www.baidu.com"

headers={ }

headers['User-Agent']="Googlebot"

request=urllib2.Request(url,headers=headers)

response=urlopen(request)

print response.read()

response.close()