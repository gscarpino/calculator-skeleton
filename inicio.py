from calculator import parse
import sys
from calculator import parse

a = sys.argv
if len(a) < 1:
	exp = raw_input('lambda> ')
else:
	i = 0
	exp = ''
	for e in a:
		if i != 0: 
			exp = exp + ' ' + e
		i = i + 1
resultado = parse(exp).eval({}).string()
resultado = resultado + ':' + parse(exp).typed({}).string()
print resultado
