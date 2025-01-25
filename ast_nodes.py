class VarDeclNode:
    def __init__(self, var_name, data_type, value):
        self.var_name = var_name
        self.data_type = data_type
        self.value = value

class VarUseNode:
    def __init__(self, var_name):
        self.var_name = var_name

class ExprNode:
    def __init__(self, expression):
        self.expression = expression

class PrintNode:
    def __init__(self, expr):
        self.expr = expr
