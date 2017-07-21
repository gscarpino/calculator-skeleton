import copy

class Expression:
    def eval(self, context):
        pass

    def typed(self, context):
        pass


class ZeroExp(Expression):
    def __init__(self):
        self.value = "0"
        self.type = NatType()

    def eval(self, context):
        return self

    def typed(self, context):
        return self.type


class BoolExp(Expression):
    def __init__(self, val):
        self.value = val
        self.type = BoolType()

    def eval(self, context):
        return self

    def typed(self, context):
        return self.type


class IfThenElseExp(Expression):
    def __init__(self, cond, exp1, exp2):
        self.cond = cond
        self.trueExp = exp1
        self.falseExp = exp2

    def eval(self, context):
        if self.cond.eval(context):
            return self.trueExp.eval(context)
        else:
            return self.falseExp.eval(context)

    def typed(self, context):
        if sameType(self.cond.typed(context), BoolType()) and sameType(self.trueExp.typed(context),self.falseExp.typed(context)):
            return self.trueExp.typed(context)
        else:
            #Error
            pass


class SuccExp(Expression):
    def __init__(self, exp):
        self.exp = exp

    def eval(self, context):
            return SuccExp(self.exp.eval(context))

    def typed(self, context):
        if sameType(self.exp.typed(context), NatType()):
            return NatType()
        else:
            #Error!
            pass

    def innerExp(self):
        return self.exp


class IsZeroExp(Expression):
    def __init__(self, exp):
        self.exp = exp

    def eval(self, context):
        return BoolExp(sameExpression(self.exp.eval(context), ZeroExp()))

    def typed(self, context):
        if sameType(self.exp.typed(context), NatType()):
            return BoolType()
        else:
            #Error!
            pass


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
            #Error!
            pass

class VarExp(Expression):
    def __init__(self, var):
        self.exp = var

    def eval(self, context):
        return context[self.exp].eval()

    def typed(self, context):
        return context[self.exp].typed()


class AbsExp(Expression):
    def __init__(self, var, type, body):
        self.var = var
        self.type = type
        self.body = body

    def eval(self, context):
        context[self.var] = copy.deepcopy(context["var"]);
        del context["var"]
        return self.body.eval(context)

    def typed(self, context):
        return self.type


class AppExp(Expression):
    def __init__(self, fun, param):
        self.fun = fun
        self.param = param

    def eval(self, context):
        context["var"] = param
        return fun.eval(context)

    def typed(self, context):
        return fun.typed()

class NatType():
    def show(self):
        print "Nat"


class BoolType():
    def show(self):
        print "Bool"

class ArrowType():
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def show(self):
        self.left.show()
        print " -> "
        self.right.show()


def sameType(t1, t2):
    return t1.show() == t2.show()
