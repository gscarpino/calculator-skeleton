#! coding: utf-8
"""Calculator lexer example."""
import ply.lex as lex

"""
Lista de tokens

El analizador léxico de PLY (al llamar al método lex.lex()) va a buscar
para cada uno de estos tokens una variable "t_TOKEN" en el módulo actual.

Sí, es súper nigromántico pero es lo que hay.

t_TOKEN puede ser:

- Una expresión regular
- Una función cuyo docstring sea una expresión regular (bizarro).

En el segundo caso, podemos hacer algunas cosas "extras", como se
muestra aquí abajo.

"""

tokens = (
    'ZERO',
    'BOOLEAN',
    'BOOL',
    'NAT',
    'PARENTESIS_ABRE',
    'PARENTESIS_CIERRA',
    'VAR',
    'IF',
    'THEN',
    'ELSE',
    'REVERSE_SLASH',
    'DOT',
    '2DOT',
    'ARROW',
    'SUCC',
    'ISZERO',
    'PRED'
)


t_BOOLEAN =  r'true|false'
t_BOOL =  r'Bool'
t_NAT =  r'Nat'
t_SUCC =  r'succ'
t_ISZERO =  r'iszero'
t_PRED =  r'pred'
t_PARENTESIS_ABRE =  r'\('
t_PARENTESIS_CIERRA =  r'\)'
t_REVERSE_SLASH = r'\\'
#t_SPACE = r'\s'
t_DOT = r'\.'
t_2DOT = r'\:'
t_ARROW = r'->'
t_ignore  = ' \t'

reserved = {
    'if' : 'IF',
    'then' : 'THEN',
    'else' : 'ELSE'
}

def t_IF(t):
    r'if'
    return t

def t_THEN(t):
    r'then'
    return t

def t_ELSE(t):
    r'else'
    return t

def t_VAR(t):
    r'a|b|c|d|e|g|h|i|j|k|l|m|n|o|p|q|r|u|v|w|x|y|z|A|C|D|E|F|G|H|I|J|K|L|M|O|P|Q|R|S|T|U|V|W|X|Y|Z'
    return t

def t_ZERO(t):
    r'0'
    t.value = "0"
    return t

# Build the lexer
lexer = lex.lex()

def apply_lexer(string):
    """Aplica el lexer al string dado."""
    lexer.input(string)

    return list(lexer)
