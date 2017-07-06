import textwrap
from textwrapexample import sample_text

print 'No dedent:\n'
print textwrap.fill(sample_text,width=50)