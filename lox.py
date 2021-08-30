from os import stat
import pathlib
import sys
import scanner
from token_type import Token_Type as TT
from token import Token
from parser import Parser
from ast_printer import Ast_Printer

class Lox:
    had_error = False

    @staticmethod
    def main():
        if len(sys.argv) == 2:
            Lox.run_file(sys.argv[1])
        else:
            Lox.run_prompt()

    @staticmethod
    def run_file(path: str):
        _bytes = pathlib.Path(path).read_bytes()
        Lox.run(_bytes)

        # Indicate an error in the exit code
        if Lox.had_error:
            exit(65)

    @staticmethod
    def run_prompt():
        while(True):
            print("> ", end="")
            line = input()
            if line == None:
                break
            Lox.run(line)
            Lox.had_error = False

    @staticmethod
    def run(source: str):
        scnr = scanner.Scanner(source)
        tokens = scnr.scan_tokens()

        parser = Parser(tokens)
        expression = parser.parse()
        if Lox.had_error: return

        print(Ast_Printer().print(expression))

    @staticmethod
    def error(line: int, message: str):
        Lox.report(line, "", message)

    @staticmethod
    def report(line: int, where: str, message: str):
        print(f"[line {line}] Error {where}: {message}")
        Lox.had_error = True

    @staticmethod
    def error(token: Token, message: str):
        if token.type == TT.EOF:
            Lox.report(token.line, " at the end", message)
        else:
            Lox.report(token.line, f" at '{token.lexeme}'", message)

if __name__ == "__main__":
    Lox.main()
