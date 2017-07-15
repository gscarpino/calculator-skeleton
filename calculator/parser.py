"""Parser LR(1) de calculadora."""
import ply.yacc as yacc
from .lexer import tokens


"""
Producciones

E -> V E | lambda
V -> true | false | 0 | if E then E else E | \S:T.E | succ(E) | pred(E) | iszero(E) | S
S -> var
T -> Bool | Nat | T -> T
"""

precedence = [
    ('right', 'REVERSE_SLASH', '2DOT', 'DOT'),
    ('right', 'IF', 'THEN', 'ELSE'),
    ('right', 'PARENTESIS_ABRE'),
    ('left', 'PARENTESIS_CIERRA'),
    ('right', 'PRED'),
    ('right', 'SUCC','ISZERO'),
    ('left', 'ZERO', 'BOOLEAN')
]


def p_expression_value(p):
    'expression : value expression'
    if p[2] == None:
        p[0] = p[1]
        pass
    else:
        #value es (var,type,expression)
        #p[0] =
        print p[1], p[2]
        typeExp = p[1][1].split("->")
        typeValue = p[2][1].split("->")
        print "exp: ", typeExp
        print "value: ",typeValue
        p[0] = p[1][2].replace(p[1][0],p[2][0])

def p_expression_lambda(p):
    'expression : '
    pass

"""def p_type_bool(p):
    'type : BOOL'
    p[0] = p[1]

def p_type_nat(p):
    'type : NAT'
    p[0] = p[1]

def p_type_arrow(p):
    'type : type ARROW type'
    p[0] = p[1] + p[2] + p[3]"""


def p_value_boolean(p):
    'value : BOOLEAN'
    p[0] = (p[1], 'Bool')

def p_value_zero(p):
    'value : ZERO'
    p[0] = ("0",'Nat')

def p_value_var(p):
    'value : var'
    p[0] = p[1]

def p_value_succ_var(p):
    'value : SUCC PARENTESIS_ABRE expression PARENTESIS_CIERRA'
    if p[3][1] == 'Nat':
        p[0] = (p[1] + p[2] + p[3][0] + p[4], "Nat")
    else:
        #TODO: control de errores
        msg("No tipa succ")
        p_error(p)

def p_value_iszero(p):
    'value : ISZERO PARENTESIS_ABRE expression PARENTESIS_CIERRA'
    if p[3][1] == 'Nat':
        p[0] = (p[3][0] == "0", "Bool")
    else:
        #TODO: control de errores
        msg("No tipa iszero")
        p_error(p)

def p_value_pred_succ(p):
    'value : PRED PARENTESIS_ABRE SUCC PARENTESIS_ABRE expression PARENTESIS_CIERRA PARENTESIS_CIERRA'
    p[0] = p[5]

def p_value_pred(p):
    'value : PRED PARENTESIS_ABRE expression PARENTESIS_CIERRA'
    if p[3][1] == 'Nat':
        if (p[3][0] == 'succ(0)' or p[3][0] == "0"):
            p[0] = ("0", "Nat")
        else:
            p[0] = (p[1] + p[2] + p[3][0] + p[4], "Nat")
    else:
        #TODO: control de errores
        msg("No tipa pred")
        p_error(p)


"""
def p_value_ite(p):
    'value : IF expression THEN expression ELSE expression'
    if p[2][1] != 'Bool':
        msg("condicion del if no es bool")
        return p_error(p)
    if p[4][1] != p[6][1]:
        msg("if con distinto tipo en lo que devuelve")
        return p_error(p)
    p[0] = p[4] if p[2][0]  == 'true' else p[6]


def p_exp_var(p):
    'expression : var'
    p[0] = p[1]


def p_value_lambda_exp(p):
    'value : REVERSE_SLASH var 2DOT type DOT expression'
    print "funcion anonima"
    p[0] = (p[2], p[4], p[6])
"""
def p_var_lambda_exp(p):
    'var : VAR'
    p[0] = p[1]

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
