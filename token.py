from token_type import Token_type

class Token:
    def __init__(self, type: Token_type, lexeme: str, literal: object, line: int):
        self.type = type
        self.lexeme = lexeme
        self.literal = literal
        self.line = line
    
    def __repr__(self) -> str:
        return "{self.type} {self.lexeme} {self.literal}"