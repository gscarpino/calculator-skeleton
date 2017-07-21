"""Archivo principal de calculadora."""
from calculator import parse

while True:
    try:
        exp_str = raw_input('lambda> ')
    except EOFError:
        break

    parse(exp_str).typed({})
    print "EVAL: "
    parse(exp_str).eval({}).show()
    print "TYPE: "
    parse(exp_str).typed({}).show()
