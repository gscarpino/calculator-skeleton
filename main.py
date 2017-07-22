"""Archivo principal de calculadora."""
from calculator import parse

while True:
    try:
        exp_str = raw_input('lambda> ')
    except EOFError:
        break

    try:
        print "TYPE: "
        print parse(exp_str).typed({}).string()
        print "EVAL: "
        print parse(exp_str).eval({}).string()
    except:
        pass
