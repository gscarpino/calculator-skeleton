"""Parser LR(1) de calculadora."""
import ply.yacc as yacc
from .lexer import tokens

def p_expression_plus(p):
    'expression : expression PLUS NUMBER'
    p[0] = p[1] + p[3]


def p_expression_term(p):
    'expression : NUMBER'
    p[0] = p[1]

def p_error(p):
    print("Hubo un error en el parseo.")

    parser.restart()


# Build the parser
parser = yacc.yacc(debug=True)

def apply_parser(str):
    return parser.parse(str)