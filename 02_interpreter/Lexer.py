from Token import Token, TokenType

class LexicalError(Exception):
    pass

class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_char: str = self.text[self.pos]

    def advance(self):
        """Переміщуємо 'вказівник' на наступний символ вхідного рядка"""
        self.pos += 1
        if self.pos > len(self.text) - 1:
            self.current_char = None  # Означає кінець введення
        else:
            self.current_char = self.text[self.pos]

    def skip_whitespace(self):
        """Пропускаємо пробільні символи."""
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def integer(self):
        """Повертаємо ціле число, зібране з послідовності цифр."""
        result = ""
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        return int(result)

    def get_next_token(self):
        """Лексичний аналізатор, що розбиває вхідний рядок на токени."""
        # check_op = 0
        # check_paren = 0
        while self.current_char is not None:
            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            if self.current_char.isdigit():
                # if check_op>1:
                #     raise LexicalError("Помилка лексичного аналізу з послідовністю операцій")
                # check_op -=1
                return Token(TokenType.INTEGER, self.integer())

            if self.current_char == "+":
                # check_op +=1
                self.advance()
                return Token(TokenType.PLUS, "+")

            if self.current_char == "-":
                # check_op +=1
                self.advance()
                return Token(TokenType.MINUS, "-")
            
            if self.current_char == "*":
                # check_op +=1
                self.advance()
                return Token(TokenType.MUL, "*")

            if self.current_char == "/":
                # check_op +=1
                self.advance()
                return Token(TokenType.DIV, "/")
            
            if self.current_char == "(":
                # check_paren += 1
                self.advance()
                return Token(TokenType.LPAREN, "(")

            if self.current_char == ")":
                # if not check_paren:
                #     raise LexicalError("Помилка лексичного аналізу з послідовністю скобок")
                # check_paren -= 1
                self.advance()
                return Token(TokenType.RPAREN, ")")

            raise LexicalError("Помилка лексичного аналізу")
        # if check_op:
        #     raise LexicalError("Помилка лексичного аналізу з послідовністю операцій")
        # if check_paren:
        #     raise LexicalError("Помилка лексичного аналізу з послідовністю скобок")
        return Token(TokenType.EOF, None)