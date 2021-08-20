from token import Token
from token_type import Token_type as TT
from lox import Lox

class Scanner:
    def __init__(self, source: str) -> None:
        self.source = source
        self.tokens = []
        self.start = 0
        self.current = 0
        self.line = 1

    def scan_tokens(self):
        while not self.is_at_end():
            self.start = self.current
            self.scan_token()
        
        self.tokens.add(Token(TT.EOF, "", None, self.line))
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
                Lox.error(self.line, "Unexpected character.")

    def string(self):
        while self.peek() != '"' and not self.is_at_end():
            if self.peek() == "\n":
                self.line += 1
            self.advance()
        
        if self.is_at_end():
            Lox.error(self.line, "Unterminated string")
            return

        # closing "
        self.advance()

        # trim off the surrounding quotes
        value = self.source[1:self.current-1]
        self.add_token(TT.STRING, value)

    def check_next(self, expected):
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

    def is_at_end(self):
        return self.current >= len(self.source)

    def advance(self):
        ret = self.source[self.current]
        self.current += 1
        return ret

    def add_token(self, type: TT, literal=None):
        text = self.source[self.start, self.current]
        self.tokens.append(Token(type, text, literal, self.line))
