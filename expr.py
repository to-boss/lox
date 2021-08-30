import lox
from token import Token
from abc import ABC, abstractmethod

class Expr(ABC):
  def __init__(self, value):
      self.value = value
      super().__init__()

  def accept(self, visitor):
      pass

class Binary(Expr):
  def __init__(self, left: Expr, operator: Token, right: Expr):
      self.left = left
      self.operator = operator
      self.right = right

  def accept(self, visitor):
      return visitor.visit_binary_expr(self)

class Grouping(Expr):
  def __init__(self, expression: Expr):
      self.expression = expression

  def accept(self, visitor):
      return visitor.visit_grouping_expr(self)

class Literal(Expr):
  def __init__(self, value: object):
      self.value = value

  def accept(self, visitor):
      return visitor.visit_literal_expr(self)

class Unary(Expr):
  def __init__(self, operator: Token, right: Expr):
      self.operator = operator
      self.right = right

  def accept(self, visitor):
      return visitor.visit_unary_expr(self)

class Visitor(Expr):
  @abstractmethod
  def visit_binary_expr(expr: Binary):
     pass

  @abstractmethod
  def visit_grouping_expr(expr: Grouping):
     pass

  @abstractmethod
  def visit_literal_expr(expr: Literal):
     pass

  @abstractmethod
  def visit_unary_expr(expr: Unary):
     pass

