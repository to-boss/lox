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

    f.write(f"  def accept(self, visitor):")
    f.write("\n")
    f.write(f"      pass")
    f.write("\n")

    f.write("\n")

    class_names = []
    for type in types:
        class_name = type.split(";")[0].strip()
        class_names.append(class_name)
        fields = type.split(";")[1].strip()
        define_type(f, base_name, class_name, fields)
        define_visitor(f, class_name, types)

    define_visitor_class(f, class_names)

    f.close()

def define_visitor_class(f, class_names):
    f.write(f"class Visitor(Expr):")
    f.write("\n")
    for name in class_names:
        f.write(f"  @abstractmethod")
        f.write("\n")
        f.write(f"  def visit_{name.lower()}_expr(expr: {name}):")
        f.write("\n")
        f.write(f"     pass")
        f.write("\n")
        f.write("\n")

def define_visitor(f, class_name, types):
    f.write(f"  def accept(self, visitor):")
    f.write("\n")
    f.write(f"      return visitor.visit_{class_name.lower()}_expr(self)")
    f.write("\n")
    f.write("\n")
    

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