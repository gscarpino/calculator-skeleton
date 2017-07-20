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
        return self.value

    def typed(self, context):
        return self.type


class BoolExp(Expression):
    def __init__(self, val):
        self.value = val
        self.type = BoolType()

    def eval(self, context):
        return self.value

    def typed(self, context):
        return self.type


class ParentesisExp(Expression):
    def __init__(self, exp):
        self.exp = exp

    def eval(self, context):
        return self.exp.eval(context)

    def typed(self, context):
        return self.exp.typed(context)


class IfThenElseExp(Expression):
    def __init__(self, cond, exp1, exp2):
        self.cond = cond
        self.trueExp = exp1
        self.falseExp = exp2

    def eval(self, context):
        if sameType(self.cond.type(context), BoolType()) and sameType(self.trueExp.typed(context),self.falseExp.typed(context)):
            if self.cond.eval(context):
                return self.trueExp.eval(context)
            else:
                return self.falseExp.eval(context)
        else:
            #Error
            pass

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
        if sameType(self.exp.typed(context), NatType()):
            return SuccExp(self.exp.eval(context))
            #return "succ(" + self.exp.eval(context) + ")"
        else:
            #Error!
            pass

    def typed(self, context):
        if sameType(self.exp.typed(context), NatType()):
            return NatType()
        else:
            #Error!
            pass


class IsZeroExp(Expression):
    def __init__(self, exp):
        self.exp = exp

    def eval(self, context):
        if sameType(self.exp.typed(context), NatType()):
            return self.exp.eval(context) == ZeroExp().eval()
            #return "iszero(" + self.exp.eval(context) + ")"
        else:
            #Error!
            pass

    def typed(self, context):
        if sameType(self.exp.typed(context), NatType()):
            return BoolType()
        else:
            #Error!
            pass

#class PredExp(Expression):
#class VarExp(Expression):
#class AbsExp(Expression):
#class AppExp(Expression):
