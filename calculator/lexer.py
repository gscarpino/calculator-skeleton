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

t_BOOL =  r'Bool'
t_NAT =  r'Nat'
t_PARENTESIS_ABRE =  r'\('
t_PARENTESIS_CIERRA =  r'\)'
t_REVERSE_SLASH = r'\\'
t_DOT = r'\.'
t_2DOT = r'\:'
t_ARROW = r'->'
t_ignore  = ' \t'

reserved = {
    'if' : 'IF',
    'then' : 'THEN',
    'else' : 'ELSE'
}


def t_SUCC(t):
    r'succ'
    return t

def t_ISZERO(t):
    r'iszero'
    return t

def t_PRED(t):
    r'pred'
    return t

def t_BOOLEAN(t):
    r'true|false'
    return t

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
    r'[a-z]{1}'
    #r'x'
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
