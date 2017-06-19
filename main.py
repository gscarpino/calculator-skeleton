"""Archivo principal de calculadora."""
from calculator import parse

while True:
    try:
        exp_str = raw_input('calc> ')
    except EOFError:
        break
    print(parse(exp_str))
