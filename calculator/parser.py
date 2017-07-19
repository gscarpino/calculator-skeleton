"""Parser LR(1) de calculadora."""
import ply.yacc as yacc
import re
from .lexer import tokens


"""
Producciones

E -> V E | lambda
V -> true | false | 0 | if E then E else E | \S:T.E | succ(E) | pred(E) | iszero(E) | S
S -> var
T -> Bool | Nat | T -> T
--------------------------------

E(expression) -> B E | \var:T.S | lambda
B(funcion) -> (E) | V | if E then E else E | succ(E) | pred(E) | iszero(E)
S(sexpression) -> F S | \var:T.S | lambda
F(sfuncion) -> var | (S) | V | if S then S else S | succ(S) | pred(S) | iszero(S)
V(value) -> true | false | 0
T(type) -> R A
R(tipo) -> Bool | Nat
A(arro) -> -> T | lambda

--------------------------------

E -> F E | V | lambda
F -> (E) | if E then E else E | succ(E) | pred(E) | iszero(E) | var
V -> true | false | 0 | X
X -> \var:T.E
T -> L R
L -> Bool | Nat
R -> -> T | lambda

"""

precedence = [
    ('right', 'REVERSE_SLASH', '2DOT', 'DOT'),
    ('left', 'PARENTESIS_CIERRA'),
    ('right', 'PARENTESIS_ABRE'),
    ('right', 'IF'),
    ('right','THEN'),
    ('right','ELSE'),
    ('right', 'PRED','ISZERO'),
    ('right', 'ZERO', 'BOOLEAN', 'SUCC', 'VAR')
]


def p_expression_value(p):
    'expression : value'
    p[0] = p[1]

def p_expression_aplicacion(p):
    'expression : term expression'
    p[0] = p[1]
    """if p[2] == None:
        if len(p[1]) == 3:
            p[0] = (p[1][0], p[1][1][2] + "->" + p[1][2])
        else:
            p[0] = (p[1][0], p[1][1])
    else:
        if p[1][1][2] != p[2][1]:
            return msg("La funcion pedia tipo " + p[1][1][2] + " y recibio tipo " + p[2][1], p)
        m = p[1][1][1].replace(p[1][1][0], p[2][0])
        p[0] = apply_parser(m)
        #TO DO el primer pedazo del tipo de 1 tieme que ser el de 2
"""
def p_expression_lambda(p):
    'expression : '
    pass

def p_value_boolean(p):
    'value : BOOLEAN'
    p[0] = [p[1], 'Bool', {}]

def p_value_zero(p):
    'value : ZERO'
    p[0] = ['0','Nat', {}]

def p_term_var(p):
    'term : var'
    p[0] = p[1]


def p_term_parentesis(p):
    'term : PARENTESIS_ABRE expression PARENTESIS_CIERRA'
    p[0] = p[2]

def p_term_succ_var(p):
    'term : SUCC PARENTESIS_ABRE expression PARENTESIS_CIERRA'
    if p[3][1] == 'undefined':
        p[3][1] = 'Nat'
        #TODO: cambiar a regexp
        if p[3][0] == 'x':
            p[0] = [p[1] + p[2] + p[3][0] + p[4], "Nat", mgu({p[3][0]: 'Nat'}, p[3][2])]
        else:
            p[0] = [p[1] + p[2] + p[3][0] + p[4], "Nat", p[3][2]]
    else:
        if p[3][1] == 'Nat':
            p[0] = [p[1] + p[2] + p[3][0] + p[4], "Nat", p[3][2]]
        else:
            #TODO: control de errores
            msg("No tipa succ")
            p_error(p)

def p_term_iszero(p):
    'term : ISZERO PARENTESIS_ABRE expression PARENTESIS_CIERRA'
    if p[3][1] == 'undefined':
        p[3][1] = 'Nat'
        #TODO: cambiar a regexp
        if p[3][0] == 'x':
            p[0] = [p[1] + p[2] + p[3][0] + p[4], "Bool", mgu({p[3][0]: 'Nat'}, p[3][2])]
        else:
            p[0] = [p[1] + p[2] + p[3][0] + p[4], "Bool", p[3][2]]
    else:
        if p[3][1] == 'Nat':
            if p[3][0] == "0":
                p[0] = ["true", "Bool", p[3][2]]
            else:
                if len(p[3][2]) > 0:
                    p[0] = [p[1] + p[2] + p[3][0] + p[4], "Bool", p[3][2]]
                else:
                    p[0] = ["false", "Bool", p[3][2]]
        else:
            #TODO: control de errores
            msg("No tipa succ")
            p_error(p)


def p_term_pred(p):
    'term : PRED PARENTESIS_ABRE expression PARENTESIS_CIERRA'
    if p[3][1] == 'undefined':
        p[3][1] = 'Nat'
        #TODO: cambiar a regexp
        if p[3][0] == 'x':
            p[0] = [p[1] + p[2] + p[3][0] + p[4], "Nat", mgu({p[3][0]: 'Nat'}, p[3][2])]
        else:
            p[0] = [p[1] + p[2] + p[3][0] + p[4], "Nat", p[3][2]]
    else:
        if p[3][1] == 'Nat':
            if (p[3][0] == "0"):
                p[0] = p[3] #("0", "Nat", {})
            else:
                m = re.search("succ\((.+)\)",p[3][0])
                if m:
                    p[0] = [m.group(1), "Nat", p[3][2]]
                else:
                    if len(p[3][2]) > 0:
                        p[0] = [p[1] + p[2] + p[3][0] + p[4], "Nat", p[3][2]]
                    else:
                        msg("No tipa pred")
                        p_error(p)
        else:
            #TODO: control de errores
            msg("No tipa pred")
            p_error(p)


def p_term_ite(p):
    'term : IF expression THEN expression ELSE expression'

    if p[2][1] == 'undefined':
        p[2][1] = 'Bool'
        #TODO: cambiar a regexp
        if [2][0] == 'x':
            p[2][2] = mgu({p[2][0]: 'Bool'}, p[2][2])
    if p[2][1] != 'Bool':
        msg("condicion del if no es bool")
        return p_error(p)
    if p[4][1] != p[6][1]:
        if p[4][1] == 'undefined':
            p[4][1] = p[6][1]
            #TODO: cambiar a regexp
            if p[4][0] == 'x':
                p[4][2] = {p[4][0]: p[6][1]}
        else:
            if p[6][1] == 'undefined':
                p[6][1] = p[4][1]
                #TODO: cambiar a regexp
                if p[6][0] == 'x':
                    p[6][2] = {p[6][0]: p[4][1]}
            else:
                msg("if con distinto tipo en lo que devuelve")
                return p_error(p)
    unifiedContext = mgu(p[4][2], p[2][2], p[6][2])
    if p[2][0] == 'true' or p[2][0] == 'false':
        if p[2][0] == 'true':
            p[4][2] = unifiedContext
            p[0] = p[4]
        else:
            p[6][2] = unifiedContext
            p[0] = p[6]
    else:
        p[0] = [p[1] + p[2][0] + p[3] + p[4][0] + p[5] + p[6][0], p[4][1], unifiedContext]



def p_type(p):
    'type : left right'
    p[0] = p[1]


def p_type_nat(p):
    'left : NAT'
    p[0] = p[1]

def p_type_bool(p):
    'left : BOOL'
    p[0] = p[1]

def p_type_arrow(p):
    'right : ARROW type'
    p[0] = p[1] + p[2] + p[3]

def p_type_lambda(p):
    'right : '
    pass

def p_var_lambda_exp(p):
    'var : VAR'
    p[0] = [p[1], 'undefined', {'x': 'undefined'}]

def p_value_lambda_exp(p):
    'value : REVERSE_SLASH var 2DOT type DOT expression'
    p[0] = [p[1] + p[2][0] + p[3] + p[4] + p[5] + p[6][0], p[4] + " -> " + p[6][1], mgu({p[2][0]: p[4]}, p[6][2])]

def msg(msg):
    print msg

def p_error(p):
    print("Hubo un error en el parseo.")
    print p
    parser.restart()

def mgu(main, *contexts):
    for context in contexts:
        for v in context.keys():
            if main.has_key(v):
                if main[v] == "undefined":
                    main[v] = context[v]
                if main[v] != context[v] and context[v] != "undefined":
                    msg("Error de tipeo, no tipa " + v + ": " + context[v] + " distinto de " + main[v])
                    p_error("Error de tipeo, no tipa " + v + ": " + context[v] + " distinto de " + main[v])
            else:
                main[v] = context[v]
            pass
        pass
    return main

# Build the parser
parser = yacc.yacc(debug=True)

def apply_parser(str):
    return parser.parse(str)

