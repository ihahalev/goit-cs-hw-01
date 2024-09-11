from __future__ import annotations
from Token import Token, TokenType
from Lexer import Lexer

class ParsingError(Exception):
    pass

class AST:
    pass

class BinOp(AST):
    def __init__(self, left:Num, op: Token, right: Num):
        self.left = left
        self.op = op
        self.right = right


class Num(AST):
    def __init__(self, token: Token):
        self.token = token
        self.value = token.value


class Parser:
    def __init__(self, lexer: Lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()

    def error(self):
        raise ParsingError("Помилка синтаксичного аналізу")

    def eat(self, token_type):
        """
        Порівнюємо поточний токен з очікуваним токеном і, якщо вони збігаються,
        'поглинаємо' його і переходимо до наступного токена.
        """
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error()

    def factor(self) -> Num | BinOp:
        token = self.current_token
        if token.type == TokenType.INTEGER:
            self.eat(TokenType.INTEGER)
            return Num(token)
        elif token.type == TokenType.LPAREN:
            self.eat(TokenType.LPAREN)
            node = self.expr()
            self.eat(TokenType.RPAREN)
            return node

    def term(self) -> Num | BinOp:
        """Парсер для 'term' правил граматики."""
        node = self.factor()
        while self.current_token.type in (TokenType.MUL, TokenType.DIV):
            token = self.current_token
            if token.type == TokenType.MUL:
                self.eat(TokenType.MUL)
            elif token.type == TokenType.DIV:
                self.eat(TokenType.DIV)

            node = BinOp(left=node, op=token, right=self.factor())
        return node

    # початок парсингу
    def expr(self) -> Num | BinOp:
        """Парсер для арифметичних виразів."""
        node = self.term()

        while self.current_token.type in (TokenType.PLUS, TokenType.MINUS):
            token = self.current_token
            if token.type == TokenType.PLUS:
                self.eat(TokenType.PLUS)
            elif token.type == TokenType.MINUS:
                self.eat(TokenType.MINUS)

            node = BinOp(left=node, op=token, right=self.term())

        return node


def print_ast(node, level=0):
    indent = "  " * level
    if isinstance(node, Num):
        print(f"{indent}Num({node.value})")
    elif isinstance(node, BinOp):
        print(f"{indent}BinOp:")
        print(f"{indent}  left: ")
        print_ast(node.left, level + 2)
        print(f"{indent}  op: {node.op.type}")
        print(f"{indent}  right: ")
        print_ast(node.right, level + 2)
    else:
        print(f"{indent}Unknown node type: {type(node)}")