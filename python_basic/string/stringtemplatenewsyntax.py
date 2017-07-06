import string
import re

class MyTemplate(string.Template):
	delimiter='{{'
	pattern=r'''
	\{\{(?:
	(?P<escaped>\{\{)|
	(?P<name>[_a-z][_a-z0-9]*)\}\}|
	(?P<braced>[_a-z][_a-z0-9]*)\}\}|
	(?P<invalid>)
	'''

t=MyTemplate('''
	{{{{
	{{var}}
	''')

print 'MATCHES:',t.pattern.findall(t.template)
print 'SUBSTITUTED:',t.safe_substitude(var='replacement')