import copy

class Expression:
    def eval(self, context):
        pass

    def typed(self, context):
        pass

    def string(self):
        pass

class ZeroExp(Expression):
    def __init__(self):
        self.value = "0"
        self.type = NatType()

    def eval(self, context):
        return self

    def typed(self, context):
        return self.type

    def string(self):
        return "0"


class BoolExp(Expression):
    def __init__(self, val):
        self.value = val
        self.type = BoolType()

    def eval(self, context):
        return self

    def typed(self, context):
        return self.type

    def string(self):
        if self.value:
            return "true"
        else:
            return "false"


class IfThenElseExp(Expression):
    def __init__(self, cond, exp1, exp2):
        self.cond = cond
        self.trueExp = exp1
        self.falseExp = exp2

    def eval(self, context):
        if self.cond.eval(context).string() == "true":
            return self.trueExp.eval(context)
        else:
            return self.falseExp.eval(context)

    def typed(self, context):
        if sameType(self.cond.typed(context), BoolType()):
            if sameType(self.trueExp.typed(context),self.falseExp.typed(context)):
                return self.trueExp.typed(context)
            else:
                #Error
                err("Las dos opciones del if deben tener el mismo tipo: \'" + self.trueExp.typed(context).string() + "\' y \'" + self.falseExp.typed(context).string() + "\'")
                pass
        else:
            #Error
            err("Condicion del if tiene que ser del tipo Bool")
            pass

    def string(self):
        return "if " + self.cond.string() + " then " + self.trueExp.string() + " else " + self.falseExp.string()


class SuccExp(Expression):
    def __init__(self, exp):
        self.exp = exp

    def eval(self, context):
        return SuccExp(self.exp.eval(context))

    def typed(self, context):
        if sameType(self.exp.typed(context), NatType()):
            return NatType()
        else:
            err("Dominio de succ tiene que ser del tipo Nat")
            pass

    def innerExp(self):
        return self.exp

    def string(self):
        return "succ(" + self.exp.string() + ")"


class IsZeroExp(Expression):
    def __init__(self, exp):
        self.exp = exp

    def eval(self, context):
        return BoolExp(sameExpression(self.exp.eval(context), ZeroExp()))

    def typed(self, context):
        if sameType(self.exp.typed(context), NatType()):
            return BoolType()
        else:
            err("Dominio de iszero tiene que ser del tipo Nat")
            pass

    def string(self):
        return "iszero(" + self.exp.string() + ")"


class PredExp(Expression):
    def __init__(self, exp):
        self.exp = exp

    def eval(self, context):
        if sameExpression(self.exp.eval(context), ZeroExp()):
            return ZeroExp()
        else:
            #Exp es una SuccExp
            return self.exp.innerExp().eval(context)

    def typed(self, context):
        if sameType(self.exp.typed(context), NatType()):
            return NatType()
        else:
            err("Dominio de pred tiene que ser del tipo Nat")
            pass

    def string(self):
        return "pred(" + self.exp.string() + ")"


class VarExp(Expression):
    def __init__(self, var):
        self.exp = var

    def eval(self, context):
        if self.exp in context:
            return context[self.exp].eval(context)
        else:
            return VarExp(self.exp)

    def typed(self, context):
        if self.exp in context:
            return context[self.exp]
        else:
            err("El termino no es cerrado (" + self.exp + " esta libre)")
            pass

    def string(self):
        return self.exp


class LambdaExp(Expression):
    def __init__(self, var, type, body):
        self.var = var
        self.type = type
        self.body = body

    def eval(self, context):
        if "var" in context:
            context[self.var.string()] = context["var"].pop();
            return self.body.eval(context)
        else:
            return LambdaExp(self.var, self.type, self.body)


    def typed(self, context):
        context[self.var.string()] = self.type
        return ArrowType(self.type, self.body.typed(context))

    def string(self):
        return "\\" + self.var.string() + ":" + self.type.string() + "." + self.body.string()


class AppExp(Expression):
    def __init__(self, fun, param):
        self.fun = fun
        self.param = param

    def eval(self, context):
        if "var" in context:
            context["var"].append(self.param)
        else:
            context["var"] = [self.param]

        return self.fun.eval(context)

    def typed(self, context):
        if sameType(self.fun.typed(context).left(), self.param.typed(context)):
            return self.fun.typed(context).right()
        else:
            err("La parte izquierda de la aplicacion (" + self.fun.string() + ") no es una funcion con dominio en " + self.param.typed(context).string())
            pass

    def string(self):
        return self.fun.string() +  "  " + self.param.string()


class NatType():
    def string(self):
        return "Nat"

    def left(self):
        err("No es una funcion")
        pass

    def right(self):
        err("No es una funcion")
        pass


class BoolType():
    def string(self):
        return "Bool"

    def left(self):
        err("No es una funcion")
        pass

    def right(self):
        err("No es una funcion")
        pass


class ArrowType():
    def __init__(self, left, right):
        self._left = left
        self._right = right

    def left(self):
        return self._left

    def right(self):
        return self._right

    def string(self):
        res = ""
        if sameType(self._left, NatType()) or sameType(self._left, BoolType()):
            res = self._left.string() + " -> "
        else:
            res = "(" + self._left.string() + ") -> "

        if sameType(self._right, NatType()) or sameType(self._right, BoolType()):
            res = res + self._right.string()
        else:
            res = res + "(" + self._right.string() + ")"

        return res


def sameType(t1, t2):
    return t1.string() == t2.string()

def sameExpression(e1, e2):
    return e1.string() == e2.string()

def err(msg):
    print "********************************************"
    print "ERROR: " + msg
    print "********************************************"

