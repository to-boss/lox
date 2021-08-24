import token_type as TT

class Token:
    def __init__(self, type: TT, lexeme: str, literal: object, line: int):
        self.type = type
        self.lexeme = lexeme
        self.literal = literal
        self.line = line
    
    def __repr__(self) -> str:
        return f"Type:{self.type}, Lexeme:{self.lexeme}, Literal:{self.literal}"