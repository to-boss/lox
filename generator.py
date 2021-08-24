import sys

def main():
    if len(sys.argv) != 1:
        print("Usage: generate_at <output directory>")
        sys.exit(64)
    output_dir = sys.argv[0]
    grammar = [
        "Binary  : Expr left, Token operator, Expr right",
        "Grouping: Expr expression",
        "Literal : Object value",
        "Unary   : Token operator, Expr right"
    ]
    define_ast(output_dir, "Expr", grammar)

def define_ast(output_dir, base_name, types):
    path = output_dir + "/" + base_name + ".py"
    f = open(path, "w")
    f.write("import lox")
    f.write("from abc import ABC, abstractmethod")
    f.write("")
    f.write(f"class {base_name}(ABC):")

    for type in types:
        class_name = type.split(":")[0].strip()
        fields = type.split(":")[1].strip()
        define_type(f, base_name, class_name, fields)

    f.close()

def define_type(f, base_name, class_name, field_list):
    # needs to be finished
    # https://craftinginterpreters.com/representing-code.html
    f.write(f"   class {class_name}({field_list}):")



if __name__ == "__main__":
    main()