import lox
import token
from abc import ABC, abstractmethod

class Expr(ABC):
  def __init__(self, value):
      self.value = value
      super().__init__()

class Binary(Expr):
  def __init__(self, left: Expr, operator: token.Token, right: Expr):
      self.left = left
      self.operator = operator
      self.right = right

class Grouping(Expr):
  def __init__(self, expression: Expr):
      self.expression = expression

class Literal(Expr):
  def __init__(self, value: object):
      self.value = value

class Unary(Expr):
  def __init__(self, operator: token.Token, right: Expr):
      self.operator = operator
      self.right = right

