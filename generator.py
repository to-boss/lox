import sys

def main():
    if len(sys.argv) != 2:
        print("Usage: generate_at <output directory>")
        sys.exit(64)
    output_dir = sys.argv[1]
    grammar = [
        "Binary  ; left: Expr, operator: token.Token, right: Expr",
        "Grouping; expression: Expr",
        "Literal ; value: object",
        "Unary   ; operator: token.Token, right: Expr"
    ]
    define_ast(output_dir, "Expr", grammar)

def define_ast(output_dir, base_name, types):
    path = output_dir + "/" + base_name.lower() + ".py"
    f = open(path, "w")
    f.write("import lox")
    f.write("\n")
    f.write("import token")
    f.write("\n")
    f.write("from abc import ABC, abstractmethod")
    f.write("\n")
    f.write("\n")
    f.write(f"class {base_name}(ABC):")
    f.write("\n")

    f.write(f"  def __init__(self, value):")
    f.write("\n")
    f.write(f"      self.value = value")
    f.write("\n")
    f.write(f"      super().__init__()")
    f.write("\n")
    f.write("\n")

    for type in types:
        class_name = type.split(";")[0].strip()
        fields = type.split(";")[1].strip()
        define_type(f, base_name, class_name, fields)

    f.close()

def define_type(f, base_name, class_name, field_list):
    # needs to be finished
    # https://craftinginterpreters.com/representing-code.html
    f.write(f"class {class_name}({base_name}):")
    f.write("\n")

    # constructor
    f.write(f"  def __init__(self, {field_list}):")
    f.write("\n")

    # store parameters in fields
    fields = field_list.split(", ")
    for field in fields:
        name = field.split(":")[0]
        f.write(f"      self.{name} = {name}")
        f.write("\n")
    
    f.write("\n")

if __name__ == "__main__":
    main()