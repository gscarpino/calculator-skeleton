"""Parser LR(1) de calculadora."""
import ply.yacc as yacc
from .lexer import tokens

"""TODO hacer lista de variables y lista de tipos"""

"""
Producciones

E(expression) -> B E | \var:T.S | lambda
B(funcion) -> (E) | V | if E then E else E | succ(E) | pred(E) | iszero(E)
S(sexpression) -> F S | \var:T.S | lambda
F(sfuncion) -> var | (S) | V | if S then S else S | succ(S) | pred(S) | iszero(S)
V(value) -> true | false | 0
T(type) -> R A
R(tipo) -> Bool | Nat 
A(arro) -> -> T | lambda
"""

"""
precedence = [
    ('right', 'REVERSE_SLASH'),
    ('right', '2DOT'),
    ('right', 'DOT')
]
"""

def p_expression_aplicacion(p):
    'expression : funcion expression'
    if p[2] == None:
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


def p_expression_funcion(p):
    'expression : REVERSE_SLASH VAR 2DOT type DOT sexpression'
    """TO DO verificar que el tipo de la variable en sexpression sea type y sea la variable var"""

    p[0] = (p[1] + p[2] + p[3] + p[4] + p[5] + p[6], (p[2], p[6], p[4]))


def p_expression_lambda(p):
    'expression : '
    pass


def p_funcion_parentesis(p):
    'funcion : PARENTESIS_ABRE expression PARENTESIS_CIERRA'
    if len(p[2]) == 3:
        p[0] = (p[2][0], p[2][1], p[2][2])
    else:
        p[0] = (p[2][0], p[2][1])


def p_funcion_value(p):
    'funcion : value'
    p[0] = p[1]


def p_funcion_ite(p):
    'funcion : IF expression THEN expression ELSE expression'
    if p[2][1] != 'Bool':
        return msg("La condicion del if espera tipo bool y recibio tipo " + p[2][1], p)
    if p[4][1] != p[6][1]:
        return msg("El if espera que la exprecion del else y del then sean del mismo tipo y recibio el then de tipo " + p[4][1] + " y el else de tipo " + p[6][1], p)
    if p[2][0] == "true":
        p[0] = p[4]
    else:
        p[0] = p[6]


def p_funcion_succ(p):
    'funcion : SUCC PARENTESIS_ABRE expression PARENTESIS_CIERRA'
    if p[3][1] == 'Nat':
            p[0] = ("succ(" + p[3][0] + ")", "Nat")
    else:
        msg("succ espera un tipo nat y recibio tipo " + p[3][1], p)


def p_funcion_pred(p):
    'funcion : PRED PARENTESIS_ABRE expression PARENTESIS_CIERRA'
    if p[3][1] == 'Nat':
        if p[3][0] == "0":
            p[0] = ("0", "Nat")
        else:
            h = p[3][0].split("(")
            f = ""
            for g in range(1, len(h)-1):
                f = f + h[g] + "("
            f = f + h[len(h)-1]
            h = f.split(")")
            f = ""
            for g in range(0, len(h)-1):
                if h[g] == "":
                    f = f + ")"
                else:
                    f = f + h[g]
            p[0] = (f, "Nat")
    else:
        msg("pred espera un tipo nat y recibio tipo " + p[3][1], p)


def p_funcion_iszero(p):
    'funcion : ISZERO PARENTESIS_ABRE expression PARENTESIS_CIERRA'
    if p[3][1] == 'Nat':
        if p[3][0] == "0":
            p[0] = ("true", "Bool")
        else:
            p[0] = ("false", "Bool")
    else:
        msg("iszero espera un tipo nat y recibio tipo " + p[3][1], p)


def p_sexpression_aplicacion(p):
    'sexpression : sfuncion sexpression'
    if p[2] == None:
        print "entre a apicacion vacia"
        #if len(p[1]) == 3:
        p[0] = p[1]
            #p[0] = (p[1][0], p[1][1] + "->" + p[1][2])
        #else:
            #p[0] = (p[1][0], p[1][1])
    else:
        print "Entre a la aplicacion"
        m = p[1][0].replace(p[1][1],p[2])
        print m
        '''if p[1][1] == "var":
            p[0] = (p[1][0] + p[2][0], "var", "->", p[2][1], "var")
        else:
            if p[2][1] == "var":

            #TO DO el primer pedazo del tipo de 1 tieme que ser el de 2
            p[0] = (p[1][0] + p[2][0], p[1][2])
    #TO DO parse(str) y parsearia supuestamente.
'''

def p_sexpression_var(p):
    'sfuncion : VAR'
#    p[0] = (p[1], "var")
    print "entre en var"
    p[0] = p[1]


def p_sexpression_funcion(p):
    'sexpression : REVERSE_SLASH VAR 2DOT type DOT sexpression'
    """TO DO verificar que el tipo de la variable en sexpression sea type y sea la variable var"""
#    p[0] = (p[1] + p[2] + p[3] + p[4] + p[5] + p[6][0], p[4], p[6][1])
    p[0] = (p[1] + p[2] + p[3] + p[4] + p[5] + p[6], p[2])


def p_sexpression_lambda(p):
    'sexpression : '
    print "entre ex lambda"
    pass


def p_sfuncion_parentesis(p):
    'sfuncion : PARENTESIS_ABRE sexpression PARENTESIS_CIERRA'
    '''if len(p[2]) == 3:
        p[0] = (p[2][0], p[2][1], p[2][2])
    else:
        p[0] = (p[2][0], p[2][1])
    '''
    p[0] = p[1] + p[2] + p[3] + p[4]

def p_sfuncion_value(p):
    'sfuncion : value'
    p[0] = p[1]


def p_sfuncion_ite(p):
    'sfuncion : IF sexpression THEN sexpression ELSE sexpression'
    tipovar = "ini"
    if p[2][1] != 'Bool' and p[2][1] != "var":
        return msg("La condicion del if espera tipo bool y recibio tipo " + p[2][1], p)
    else:
        if p[2][1] == "var":
            tipovar = "Bool"
    tipo = "ini"
    if p[4][1] != p[6][1]:
        if p[4][1] == "var":
            tipo = p[6][1]
            tipovar = p[6][1]
        else:
            if p[6][1] == "var":
                tipo = p[4][1]
                tipovar = p[4][1]
            else:
                return msg("El if espera que la exprecion del else y del then sean del mismo tipo y recibio el then de tipo " + p[4][1] + " y el else de tipo " + p[6][1], p)
    else:
        tipo = p[4][1]
        if p[6][1] == "var":
            tipovar = "var"
    p[0] = (p[1] + p[2][0] + p[3] + p[4][0] + p[5] + p[6][0], tipo, tipovar)

def p_sfuncion_succ(p):
    'sfuncion : SUCC PARENTESIS_ABRE sexpression PARENTESIS_CIERRA'
    '''if p[3][1] == 'Nat':
            p[0] = ("succ(" + p[3][0] + ")", "Nat")
    else:
        msg("succ espera un tipo nat y recibio tipo " + p[3][1], p)
    '''
    p[0] = (p[1] + p[2] + p[3][0] + p[4], "Nat")


def p_sfuncion_pred(p):
    'sfuncion : PRED PARENTESIS_ABRE sexpression PARENTESIS_CIERRA'
    '''if p[3][1] == 'Nat':
        if p[3][0] == "0":
            p[0] = ("0", "Nat")
        else:
            h = p[3][0].split("(")
            f = ""
            for g in range(1, len(h)-1):
                f = f + h[g] + "("
            f = f + h[len(h)-1]
            h = f.split(")")
            f = ""
            for g in range(0, len(h)-1):
                if h[g] == "":
                    f = f + ")"
                else:
                    f = f + h[g]
            p[0] = (f, "Nat")
    else:
        msg("pred espera un tipo nat y recibio tipo " + p[3][1], p)
    '''
    p[0] = (p[1] + p[2] + p[3][0] + p[4], "Nat")

def p_sfuncion_iszero(p):
    'sfuncion : ISZERO PARENTESIS_ABRE sexpression PARENTESIS_CIERRA'
    '''if p[3][1] == 'Nat':
        if p[3][0] == "0":
            p[0] = ("true", "Bool")
        else:
            p[0] = ("false", "Bool")
    else:
        msg("iszero espera un tipo nat y recibio tipo " + p[3][1], p)
    '''
    p[0] = (p[1] + p[2] + p[3][0] + p[4], "Bool")

def p_value_boolean(p):
    'value : BOOLEAN'
    p[0] = (p[1], "Bool")


def p_value_zero(p):
    'value : ZERO'
    p[0] = ("0", "Nat")


def p_type_arro(p):
    'type : tipo arro'
    if p[2] == None:
        p[0] = p[1]
    else:
        p[0] = p[1] + p[2]


def p_tipo_bool(p):
    'tipo : BOOL'
    p[0] = p[1]


def p_tipo_nat(p):
    'tipo : NAT'
    p[0] = p[1]


def p_arro_type(p):
    'arro : ARROW type'
    p[0] = p[1] + p[2]


def p_arro_lambda(p):
    'arro : '
    pass



def msg(msg, p):
    print msg
    p_error(p)

def p_error(p):
    print("Hubo un error en el parseo.")

    parser.restart()


# Build the parser
parser = yacc.yacc(debug=True)

def apply_parser(str):
    return parser.parse(str)