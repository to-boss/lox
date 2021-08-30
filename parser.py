from token_type import Token_Type as TT
from token import Token
from expr import *
from builtins import Exception

class Parser:
    class Parse_Error(Exception):
        def __str__(self):
            return f"Parse Error"

    def __init__(self, tokens=[]):
        self.tokens = tokens
        self.current = 0

    def parse(self) -> Expr:
        try:
            return self.expression()
        except self.Parse_Error:
            return None
        
    def expression(self) -> Expr:
        return self.equality()

    def equality(self) -> Expr:
        expr = self.comparison()

        while self.match(TT.BANG_EQUAL, TT.EQUAL_EQUAL):
            operator = self.previous()
            right = self.comparison()
            expr = Binary(expr, operator, right)
        
        return expr

    def comparison(self) -> Expr:
        expr = self.term()

        while self.match(TT.GREATER, TT.GREATER_EQUAL, TT.LESS, TT.LESS_EQUAL):
            operator = self.previous()
            right = self.term()
            expr = Binary(expr, operator, right)

        return expr

    def term(self) -> Expr:
        expr = self.factor()

        while self.match(TT.MINUS, TT.PLUS):
            operator = self.previous()
            right = self.factor()
            expr = Binary(expr, operator, right)

        return expr

    def factor(self) -> Expr:
        expr = self.unary()

        while self.match(TT.SLASH, TT.STAR):
            operator = self.previous()
            right = self.unary()
            expr = Binary(expr, operator, right)

        return expr

    def unary(self) -> Expr:
        if self.match(TT.BANG, TT.MINUS):
            operator = self.previous()
            right = self.unary()
            return Unary(operator, right)

        return self.primary()

    def primary(self) -> Expr:
        if self.match(TT.FALSE): return Literal(False)
        if self.match(TT.TRUE): return Literal(True)
        if self.match(TT.NIL): return Literal(None)

        if self.match(TT.NUMBER, TT.STRING):
            return Literal(self.previous().literal)

        if self.match(TT.LEFT_PAREN):
            expr = self.expression()
            self.consume(TT.RIGHT_PAREN, "Expect ')' after expression.")
            return Grouping(expr)

        raise self.error(self.peek(), "Expect expression")

    def match(self, *types: TT) -> bool:
        for type in types:
            if self.check(type):
                self.advance()
                return True
        
        return False

    def consume(self, type: TT, messeage: str) -> Token:
        if self.check(type):
            return self.advance()

        raise self.error(self.peek(), messeage)

    def check(self, type: TT) -> bool:
        if self.is_at_end():
            return False
        return self.peek().type == type

    def advance(self) -> Token:
        if not self.is_at_end():
            self.current += 1
        return self.previous()

    def is_at_end(self) -> bool:
        return self.peek().type == TT.EOF

    def peek(self) -> Token:
        return self.tokens[self.current]

    def previous(self) -> Token:
        return self.tokens[self.current -1]
    
    def error(self, token: Token, messeage: str) -> Parse_Error:
        lox.Lox.error(token, messeage)
        return self.Parse_Error()

    def synchronize(self):
        self.advance()

        while not self.is_at_end():
            if self.previous().type == TT.SEMICOLON: return

            match self.peek().type:
                case TT.CLASS:
                    return
                case TT.FUN:
                    return
                case TT.VAR:
                    return
                case TT.FOR:
                    return
                case TT.IF:
                    return
                case TT.WHILE:
                    return
                case TT.PRINT:
                    return
                case TT.RETURN:
                    return

            self.advance()