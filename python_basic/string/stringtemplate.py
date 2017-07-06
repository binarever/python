import string

values={'var':'foo'}

t=string.Template("""
	Variable:		$var
	Escape:			$s
	Variable in text:  $(var)iable
	""")

print 'TEMPLATE:',  t.substitute(values)

s="""
Variable:		%(var)s
Escape:			%%
Variable in text:  %(var)siable
"""

print 'INTERPOLATION:',   s  %  values