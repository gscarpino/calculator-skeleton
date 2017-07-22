"""Parser LR(1) de calculadora."""
import ply.yacc as yacc
import re
from .lexer import tokens
from exp import *


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
    ('nonassoc', 'VAR', 'PARENTESIS_ABRE', 'ISZERO', 'PRED', 'SUCC', 'ZERO', 'BOOL'),
    ('left', 'APP'),
    ('right', 'ARROW')
]

def p_expression_main(p):
    'exp : expression'
    p[0] = p[1]

def p_expression_aplicacion(p):
    'expression : expression expression %prec APP'
    p[0] = AppExp(p[1], p[2])

def p_value_boolean(p):
    'expression : BOOLEAN'
    p[0] = BoolExp(p[1] == 'true')

def p_value_zero(p):
    'expression : ZERO'
    p[0] = ZeroExp()

def p_term_var(p):
    'expression : var'
    p[0] = p[1]

def p_term_parentesis(p):
    'expression : PARENTESIS_ABRE expression PARENTESIS_CIERRA'
    p[0] = p[2]

def p_term_succ_var(p):
    'expression : SUCC PARENTESIS_ABRE expression PARENTESIS_CIERRA'
    p[0] = SuccExp(p[3])

def p_term_iszero(p):
    'expression : ISZERO PARENTESIS_ABRE expression PARENTESIS_CIERRA'
    p[0] = IsZeroExp(p[3])

def p_term_pred(p):
    'expression : PRED PARENTESIS_ABRE expression PARENTESIS_CIERRA'
    p[0] = PredExp(p[3])

def p_term_ite(p):
    'expression : IF expression THEN expression ELSE expression %prec IF'
    p[0] = IfThenElseExp(p[2], p[4], p[6])

def p_type_nat(p):
    'type : NAT'
    p[0] = NatType()

def p_type_bool(p):
    'type : BOOL'
    p[0] = BoolType()

def p_type_arrow(p):
    'type : type ARROW type'
    p[0] = ArrowType(p[1],p[3])

def p_var_lambda_exp(p):
    'var : VAR'
    p[0] = VarExp(p[1])

def p_value_lambda_exp(p):
    'expression : REVERSE_SLASH var 2DOT type DOT expression %prec REVERSE_SLASH'
    p[0] = LambdaExp(p[2], p[4], p[6])

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

