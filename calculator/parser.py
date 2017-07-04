"""Parser LR(1) de calculadora."""
import ply.yacc as yacc
from .lexer import tokens


"""
Producciones

E -> VE | lambda
V -> true | false | N | if E then E else E | \S:T.E | succ(E) | pred(E) | iszero(E)
S -> var
N -> num
T -> Bool | Nat | T -> T
"""

def p_expression_value(p):
    'expression : value'
    p[0] = p[1]

def p_term_bool(p):
    'term : BOOL'
    p[0] = p[1]

def p_term_nat(p):
    'term : NAT'
    p[0] = p[1]

def p_term_arrow(p):
    'term : term ARROW term'
    p[0] = p[1] + p[2] + p[3]

def p_number_num(p):
    'number : NUMBER'
    p[0] = p[1]

def p_value_ite(p):
    'value : IF value THEN value ELSE value'
    p[0] = p[4] if p[2] == 'true' else p[6]

def p_value_boolean(p):
    'value : BOOLEAN'
    p[0] = p[1]

def p_value_num(p):
    'value : number'
    p[0] = p[1]

def p_value_succ(p):
    'value : SUCC PARENTESIS_ABRE number PARENTESIS_CIERRA'
    p[0] = str(int(p[3]) + 1)

def p_value_pred(p):
    'value : PRED PARENTESIS_ABRE number PARENTESIS_CIERRA'
    p[0] = str(int(p[3]) - 1)

def p_value_iszero(p):
    'value : ISZERO PARENTESIS_ABRE number PARENTESIS_CIERRA'
    p[0] = str(int(p[3]) == 0)

def p_value_lambda_exp(p):
    'value : REVERSE_SLASH var 2DOT term DOT value'
    #Falla cuando se usa var en value
    p[0] = (p[2], p[6])

def p_val(p):
    'val : value'
    p[0] = p[1]

def p_value_app(p):
    'value : val value'
    #Falta probar
    p[0] = p[1][1].replace(p[1][0],p[2])

def p_var_lambda_exp(p):
    'var : VAR'
    p[0] = p[1]


def p_error(p):
    print("Hubo un error en el parseo.")

    parser.restart()


# Build the parser
parser = yacc.yacc(debug=True)

def apply_parser(str):
    return parser.parse(str)
