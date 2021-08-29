from token import *
from token_type import Token_type as TT
from expr import *

class ast_printer(Visitor):
    def __init__(self):
        pass

    def parenthesize(self, name, *exprs):
        string = f"({name}"
        for expr in exprs:
            string += f" {expr.accept(self)}"
        string += ")"

        return string

    def print(self, expr):
        return expr.accept(self)

    def visit_binary_expr(self, expr: Binary):
        return self.parenthesize(expr.operator.lexeme, expr.left, expr.right)

    def visit_grouping_expr(self, expr: Grouping):
        return self.parenthesize("group", expr.expression)

    def visit_literal_expr(self, expr: Literal):
        if expr.value == None:
            return "nil"
        return expr.value

    def visit_unary_expr(self, expr: Unary):
        return self.parenthesize(expr.operator.lexeme, expr.right)

def main():
    expression = Binary(
        Unary(
            Token(TT.MINUS, "-", None, 1), 
            Literal(123)), 
            Token(TT.STAR, "*", None, 1),
        Grouping(
            Literal(45.67)))
    printer = ast_printer()
    print(printer.print(expression))

if __name__ == "__main__":
    main()




    