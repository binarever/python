import textwrap
from textwrapexample import sample_text

dedented_text=textwrap.dedent(sample_text).strip()
for width in (45,70):
	print '%d Columns\n'%width
	print textwrap.fill(dedented_text,width=45)
	print