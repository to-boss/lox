import pathlib
import sys
import scanner

class Lox:
    had_error = False

    @staticmethod
    def main():
        if len(sys.argv) < 1:
            print("Usage: python lox.py [script]")
            exit()
        elif len(sys.argv) == 1:
            Lox.run_file(sys.argv[0])
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

        for token in tokens:
            print(token)

    @staticmethod
    def error(line: int, message: str):
        Lox.report(line, "", message)

    @staticmethod
    def report(line: int, where: str, message: str):
        print(f"[line {line}] Error {where}: {message}")
        Lox.had_error = True

if __name__ == "__main__":
    Lox.main()
