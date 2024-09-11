from Token import TokenType
from Parser import Parser, BinOp, Num

class Interpreter:
    def __init__(self, parser: Parser):
        self.parser = parser

    def visit_BinOp(self, node: BinOp):
        if node.op.type == TokenType.PLUS:
            return self.visit(node.left) + self.visit(node.right)
        elif node.op.type == TokenType.MINUS:
            return self.visit(node.left) - self.visit(node.right)
        elif node.op.type == TokenType.DIV:
            right = self.visit(node.right)
            if not right:
                raise ZeroDivisionError
            return self.visit(node.left) / right
        elif node.op.type == TokenType.MUL:
            return self.visit(node.left) * self.visit(node.right)

    def visit_Num(self, node: Num):
        return node.value

    def interpret(self):
        tree = self.parser.expr()
        return self.visit(tree)

    def visit(self, node: BinOp | Num):
        # генеруємо назву методу поточного класу
        method_name = "visit_" + type(node).__name__
        # отримуємо сам метод через вбудовану ф-ю getattr
        visitor = getattr(self, method_name, self.generic_visit)
        # запускаємо метод класу
        return visitor(node)

    def generic_visit(self, node):
        raise Exception(f"Немає методу visit_{type(node).__name__}")