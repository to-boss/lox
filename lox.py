import pathlib
from scanner import Scanner

class Lox:
    had_error = False

    @staticmethod
    def main(args: str):
        if len(args) < 1:
            print("Usage: python lox.py [script]")
            exit()
        elif len(args) == 1:
            Lox.run_file(args[0])
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
        scanner = Scanner(source)
        tokens = scanner.scan_tokens()

        for token in tokens:
            print(token)

    @staticmethod
    def error(line: int, message: str):
        Lox.report(line, "", message)

    @staticmethod
    def report(line: int, where: str, message: str):
        print("[line {line}] Error {where}: {message}")
        had_error = True


