import re

class LexerError(Exception):
    """Custom exception for lexer errors."""
    pass

class Lexer:
    def __init__(self, source_code):
        self.source_code = source_code
        self.tokens = []
        self.position = 0

    def tokenize(self):
        """
        Tokenizes the source code into a list of tokens.
        """
        token_specifications = [
            ('PRINT', r'spit_it_out'),                   # Print statement
            ('SCAN', r'gimme_that'),                    # Input statement
            ('FR', r'FR'),                              # Variable declaration keyword
            ('DATATYPE', r'int|char|float|double|string|NoCap|Tbh'), # Data types
            ('FUNCTION', r'Brew'),                      # Function declaration keyword
            ('RETURN', r'spill'),                       # Return statement
            ('IF', r'Lowkey'),                          # If statement
            ('ELSE', r'orNah'),                         # Else statement
            ('IDENTIFIER', r'wtl_[a-zA-Z_][a-zA-Z0-9_]*'), # Identifier
            ('NUMBER', r'\d+(\.\d+)?'),                 # Numbers (integers and floats)
            ('STRING', r'"[^"]*"'),                     # Strings
            ('CHAR', r"'.'"),                           # Character
            ('ASSIGN', r'='),                           # Assignment operator
            ('SEMICOLON', r';'),                        # Semicolon
            ('LPAREN', r'\('),                          # Left parenthesis
            ('RPAREN', r'\)'),                          # Right parenthesis
            ('LBRACE', r'\{'),                          # Left brace
            ('RBRACE', r'\}'),                          # Right brace
            ('OPERATOR', r'[+\-*/]'),                   # Arithmetic operators
            ('WHITESPACE', r'[ \t\n]+'),                # Whitespace (ignored)
            ('INVALID', r'.'),                          # Any invalid token
        ]

        token_regex = '|'.join(f'(?P<{pair[0]}>{pair[1]})' for pair in token_specifications)
        regex = re.compile(token_regex)

        for match in regex.finditer(self.source_code):
            kind = match.lastgroup
            value = match.group(kind)

            if kind == 'WHITESPACE':
                continue  # Ignore whitespace
            elif kind == 'INVALID':
                raise LexerError(f"Your Syntax is sus T_T at position {self.position}: {value}")
            else:
                self.tokens.append((kind, value))
            self.position += len(value)

        return self.tokens
