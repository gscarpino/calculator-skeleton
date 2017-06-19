"""Archivo principal de calculadora."""
from calculator import parse

while True:
    try:
        s = input('calc> ')
    except EOFError:
        break
    print(parse(s))
