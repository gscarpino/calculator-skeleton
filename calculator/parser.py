"""Parser LR(1) de calculadora."""
import ply.yacc as yacc
import re
from .lexer import tokens
import exp


"""
Producciones

E -> (E) | if E then E else E | succ(E) | pred(E) | iszero(E) | var
E -> true | false | 0
E -> \var:T.E
E -> E E
T -> Bool | Nat
T -> T -> T

"""

precedence = [
    ('left', 'REVERSE_SLASH'),
    ('left', 'IF'),
    ('left', 'APP'),
    ('right', 'ARROW')
]

def p_expression_aplicacion(p):
    'expression : expression expression %prec APP'

def p_value_boolean(p):
    'expression : BOOLEAN'

def p_value_zero(p):
    'expression : ZERO'

def p_term_var(p):
    'expression : var'

def p_term_parentesis(p):
    'expression : PARENTESIS_ABRE expression PARENTESIS_CIERRA'
    p[0] = p[2]

def p_term_succ_var(p):
    'expression : SUCC PARENTESIS_ABRE expression PARENTESIS_CIERRA'

def p_term_iszero(p):
    'expression : ISZERO PARENTESIS_ABRE expression PARENTESIS_CIERRA'

def p_term_pred(p):
    'expression : PRED PARENTESIS_ABRE expression PARENTESIS_CIERRA'

def p_term_ite(p):
    'expression : IF expression THEN expression ELSE expression %prec IF'

def p_type_nat(p):
    'type : NAT'

def p_type_bool(p):
    'type : BOOL'

def p_type_arrow(p):
    'type : type ARROW type'


def p_var_lambda_exp(p):
    'var : VAR'

def p_value_lambda_exp(p):
    'expression : REVERSE_SLASH var 2DOT type DOT expression %prec REVERSE_SLASH'

def msg(msg):
    print msg

def p_error(p):
    print("Hubo un error en el parseo.")
    print p
    parser.restart()

# Build the parser
parser = yacc.yacc(debug=True)

def apply_parser(str):
    return parser.parse(str)

