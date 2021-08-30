from token import Token
from token_type import Token_Type as TT
import lox

class Scanner:
    def __init__(self, source: str) -> None:
        self.source = source
        self.tokens = []
        self.start = 0
        self.current = 0
        self.line = 1

        self.keywords = {
            "and":TT.AND,
            "class":TT.CLASS,
            "else":TT.ELSE,
            "false":TT.FALSE,
            "for":TT.FOR,
            "fun":TT.FUN,
            "if":TT.IF,
            "nil":TT.NIL,
            "or":TT.OR,
            "print":TT.PRINT,
            "return":TT.RETURN,
            "super":TT.SUPER,
            "this":TT.THIS,
            "true":TT.TRUE,
            "var":TT.VAR,
            "while":TT.WHILE
        }

    def scan_tokens(self):
        while not self.is_at_end():
            self.start = self.current
            self.scan_token()
        
        self.tokens.append(Token(TT.EOF, "", None, self.line))
        return self.tokens

    def scan_token(self):
        c = self.advance()

        match c:
            case "(":
                self.add_token(TT.LEFT_PAREN)
            case ")":
                self.add_token(TT.RIGHT_PAREN)
            case "{":
                self.add_token(TT.LEFT_BRACE)
            case "}":
                self.add_token(TT.RIGHT_BRACE)
            case ",":
                self.add_token(TT.COMMA)
            case ".":
                self.add_token(TT.DOT)
            case "-":
                self.add_token(TT.MINUS)
            case "+":
                self.add_token(TT.PLUS)
            case ";":
                self.add_token(TT.SEMICOLON)
            case "*":
                self.add_token(TT.STAR)
            case "!":
                self.add_token(TT.BANG_EQUAL if self.check_next("=") else TT.BANG)
            case "=":
                self.add_token(TT.EQUAL_EQUAL if self.check_next("=") else TT.EQUAL)
            case "<":
                self.add_token(TT.LESS_EQUAL if self.check_next("=") else TT.LESS)
            case ">":
                self.add_token(TT.GREATER if self.check_next("=") else TT.GREATER)
            case "/":
                if self.check_next("/"):
                    while self.peek() != "/n" and not self.is_at_end():
                        self.advance()
                else:
                    self.add_token(TT.SLASH)
            case " ":
                pass
            case "\r":
                pass
            case "\t":
                pass
            case "\n":
                self.line += 1
            case '"':
                self.string()
            case _:
                if self.is_digit(c):
                    self.number()
                elif self.is_alpha(c):
                    self.identifier()
                else:
                    lox.Lox.error(self.line, f"Unexpected character '{c}'")

    def identifier(self):
        while self.is_alpha_numeric(self.peek()):
            self.advance()

        text = self.source[self.start:self.current]
        ttype = self.keywords.get(text)
        if ttype == None:
            ttype = TT.IDENTIFIER
        self.add_token(ttype)

    def number(self):
        while self.is_digit(self.peek()):
            self.advance()
        
        # consume . between number parts
        if self.peek() == "." and self.is_digit(self.peek_next()):
            self.advance()

            while self.is_digit(self.peek()):
                self.advance()

        self.add_token(TT.NUMBER, float(self.source[self.start:self.current]))

    def string(self):
        while self.peek() != '"' and not self.is_at_end():
            if self.peek() == "\n":
                self.line += 1
            self.advance()
        
        if self.is_at_end():
            lox.Lox.error(self.line, "Unterminated string")
            return

        # closing "
        self.advance()

        # trim off the surrounding quotes
        value = self.source[self.start+1:self.current-1]
        self.add_token(TT.STRING, value)

    def check_next(self, expected: str):
        if self.is_at_end():
            return False
        if self.source[self.current] != expected:
            return False

        self.current += 1
        return True

    def peek(self):
        if self.is_at_end():
            return "\0"
        return self.source[self.current]

    def peek_next(self):
        if self.current+1 >= len(self.source):
            return "\0"
        return self.source[self.current+1]

    def is_alpha(self, c: str):
        return (c >= "a" and c <= "z") or (c >= "A" and c <= "Z") or c == "_"

    def is_alpha_numeric(self, c: str):
        return self.is_alpha(c) or self.is_digit(c)

    def is_digit(self, c: str):
        return c >= "0" and c <= "9"

    def is_at_end(self):
        return self.current >= len(self.source)

    def advance(self):
        ret = self.source[self.current]
        self.current += 1
        return ret

    def add_token(self, type: TT, literal=None):
        text = self.source[self.start:self.current]
        self.tokens.append(Token(type, text, literal, self.line))
