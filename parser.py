from lexer import Lexer, LexerError
from collections import deque

class ParserError(Exception):
    """Custom exception for parser errors."""
    pass

# AST Node Definitions
class ASTNode:
    pass

class PrintNode(ASTNode):
    def __init__(self, expr):
        """
        Initialize a PrintNode.
        :param expr: The expression to be printed, could be an ExprNode or StringNode.
        """
        self.expr = expr

    def __repr__(self):
        # Check the type of expr and represent accordingly
        if isinstance(self.expr, StringNode):
            return f'PrintNode(expr={repr(self.expr)})'  # If it's a string, show its value
        elif isinstance(self.expr, ExprNode):
            return f'PrintNode(expr={repr(self.expr)})'  # If it's an expression, show it as well
        else:
            return f'PrintNode(expr=UnknownType)'

class StringNode:
    def __init__(self, value):
        self.value = value  # The string literal value

    def __repr__(self):
        return f'StringNode(value="{self.value}")'


class AssignmentNode:
    def __init__(self, lhs, rhs):
        self.lhs = lhs  # LHS is the identifier (variable)
        self.rhs = rhs  # RHS is the expression (could be an identifier, number, etc.)

    def __repr__(self):
        return f"AssignmentNode(lhs={self.lhs}, rhs={self.rhs})"


class VarDeclNode(ASTNode):
    def __init__(self, data_type, var_name, expr):
        self.data_type = data_type
        self.var_name = var_name
        self.expr = expr

class VarUseNode:
    def __init__(self, var_name):
        self.var_name = var_name  # The name of the variable being used

    def __repr__(self):
        return f"VarUseNode(var_name={self.var_name})"


class IfNode(ASTNode):
    def __init__(self, condition, if_block, else_block):
        self.condition = condition
        self.if_block = if_block
        self.else_block = else_block

class FuncDeclNode(ASTNode):
    def __init__(self, return_type, func_name, params, body):
        self.return_type = return_type
        self.func_name = func_name
        self.params = params
        self.body = body

class ExprNode(ASTNode):
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right

class NumberNode(ASTNode):
    def __init__(self, value):
        self.value = value

class StringNode:
    def __init__(self, value):
        self.value = value  # The string literal value

    def __repr__(self):
        return f'StringNode(value="{self.value}")'

class IdentifierNode(ASTNode):
    def __init__(self, name):
        self.name = name
        
# AST Node Definitions (extended for arithmetic operations)
class AddNode(ASTNode):
    def __init__(self, left, right):
        self.left = left
        self.right = right

class SubNode(ASTNode):
    def __init__(self, left, right):
        self.left = left
        self.right = right

class MulNode(ASTNode):
    def __init__(self, left, right):
        self.left = left
        self.right = right

class DivNode(ASTNode):
    def __init__(self, left, right):
        self.left = left
        self.right = right

class ModNode(ASTNode):
    def __init__(self, left, right):
        self.left = left
        self.right = right

class ScanStmtNode:
    def __init__(self, var_name):
        """
        Represents a SCAN statement.
        :param var_name: The name of the variable to store the input.
        """
        self.var_name = var_name

    def __repr__(self):
        """
        String representation of the ScanStmtNode.
        Example: SCAN x;
        """
        return f"ScanStmtNode(var_name='{self.var_name}')"

    def evaluate(self, context):
        """
        Evaluates the SCAN statement in the given context.
        :param context: A dictionary representing the variable environment.
        :return: Updates the context with the user input for the variable.
        """
        user_input = input(f"Enter value for {self.var_name}: ")
        context[self.var_name] = user_input


# Updated Parser Class
class Parser:
    def __init__(self, tokens):
        self.tokens = deque(tokens)  # Initialize as a deque
        self.current_token = None
        self.advance()  # Set the first token

    def advance(self):
        # Safely fetch the next token or set None if empty
        if self.tokens:  # Check if there are tokens left
            self.current_token = self.tokens.popleft()  # Move to the next token
        else:
            self.current_token = None  # No more tokens, end of input
        print(f"Advanced to next token: {self.current_token}")

    def consume(self, expected_token_type, error_message=None):
        """
        Ensures the current token matches the expected type and advances to the next token.
        :param expected_token_type: The expected type of the current token.
        :param error_message: Custom error message if the token type does not match.
        :raises ParserError: If the current token does not match the expected type.
        """
        if self.current_token[0] == expected_token_type:
            self.advance()  # Consume and move to the next token
        else:
            if error_message:
                raise ParserError(error_message)
            else:
                raise ParserError(f"Expected '{expected_token_type}', but found '{self.current_token}'")

    def next_token(self):
        if self.tokens:
            return self.tokens[0]  # Peek at the next token
        else:
            return None

    def parse(self):
        """Start the parsing process and return the AST."""
        return self.program()

    def program(self):
        """Parse the program: a list of statements."""
        statements = []
        while self.current_token:
            statements.append(self.statement())
        return statements

    def statement(self):
        """Parse a statement, which could be different types."""
        if self.current_token[0] == 'PRINT':
            return self.print_stmt()
        elif self.current_token[0] == 'SCAN':
            return self.scan_stmt()
        elif self.current_token[0] == 'FR':
            return self.var_decl()
        elif self.current_token[0] == 'Brew':
            return self.func_decl()
        elif self.current_token[0] == 'Lowkey':
            return self.if_stmt()
        elif self.current_token[0] == 'IDENTIFIER':
            return self.assignment_stmt()
        else:
            raise ParserError("Syntax error: unexpected token '{}'".format(self.current_token[1]))

    def print_stmt(self):
        """Parse a print statement."""
        self.advance()  # Skip 'PRINT'
    
        # Check if it's a string literal
        if self.current_token[0] == 'STRING':
            string_value = self.current_token[1]
            #print(string_value)
            self.advance()  # Skip the string token
            self.expect('SEMICOLON')  # Ensure the statement ends with a semicolon
            return PrintNode(string_value)  # Return a PrintNode with the string
        else:
            # Otherwise, parse it as an expression
            expr = self.expr()
            self.expect('SEMICOLON')
            return PrintNode(expr)
        
    def assignment_stmt(self):
        """Parse an assignment statement and return an AST node."""
        # LHS is an identifier
        lhs = self.current_token[1]  # Store the identifier
        self.consume('IDENTIFIER')    # Consume the identifier token

        # Check for '=' assignment operator
        self.consume('ASSIGN')        # Consume the assignment operator '='

        # Parse the right-hand side (RHS) expression
        rhs = self.expr()             # Assuming expr() parses the right-hand side

        # Return an AST node for the assignment
        return AssignmentNode(lhs, rhs)


    def expr(self):
        """Parse an expression (handles addition and subtraction)."""
        left = self.term()  # Start with the first term

        while self.current_token and self.current_token[0] in   ('OPERATOR') and self.current_token[1] in ('+', '-'):
            operator = self.current_token[1]
            self.advance()  # Skip operator

            # If the current token is an identifier, handle it  as a variable use
            if self.current_token[0] == 'IDENTIFIER':
                var_name = self.current_token[1]  # Get the     name of the variable
                left = VarUseNode(var_name)  # Create a  VarUseNode for variable usage
                self.advance()  # Consume the identifier token
            else:
               right = self.term()  # Otherwise, continue  parsing the right side of the expression

            # Handle the addition or subtraction
            if operator == '+':
                left = AddNode(left, right)
            elif operator == '-':
                left = SubNode(left, right)

        return left

    def term(self):
        """Parse a term (handles multiplication, division, and modulus)."""
        left = self.factor()
        while self.current_token and self.current_token[0] in ('OPERATOR') and self.current_token[1] in ('*', '/', '%'):
            operator = self.current_token[1]
            self.advance()  # Skip operator
            right = self.factor()
            if operator == '*':
                left = MulNode(left, right)
            elif operator == '/':
                left = DivNode(left, right)
            elif operator == '%':
                left = ModNode(left, right)
        return left

    def factor(self):
        """Parse a factor (handles parentheses, numbers, and identifiers)."""
        if self.current_token[0] == 'NUMBER':
            value = self.current_token[1]
            self.advance()
            return NumberNode(value)
        elif self.current_token[0] == 'IDENTIFIER':
            name = self.current_token[1]
            self.advance()
            return IdentifierNode(name)
        elif self.current_token[0] == 'LPAREN':
            self.advance()
            expr = self.expr()
            self.expect('RPAREN')
            return expr
        else:
            raise ParserError("Syntax error: unexpected token '{}'".format(self.current_token[1]))

    def expect(self, token_type):
        """Helper to expect a certain token type and advance."""
        if self.current_token and self.current_token[0] == token_type:
            value = self.current_token[1]
            self.advance()
            return value
        else:
            raise ParserError(f"Expected '{token_type}', but found '{self.current_token}'")
    
    def var_decl(self):
        """
        Parse a variable declaration.
        Example: FR int x = 10;
        """
        if self.current_token[0] == "FR":
            self.consume("FR")  # Consume 'FR'

            # Parse the data type
            if self.current_token[0] == "DATATYPE":
                data_type = self.current_token[0]
                self.consume("DATATYPE")  # Consume the data type

                # Parse the variable name
                if self.current_token[0] == "IDENTIFIER":
                    var_name = self.current_token[1]
                    self.consume("IDENTIFIER")

                    # Parse the assignment (optional)
                    if self.current_token[0] == "ASSIGN":
                        self.consume("ASSIGN")
                        value = self.expr()  # Parse the expression after '='
                    else:
                        value = None  # No value assigned

                    # Consume the semicolon
                    if self.current_token[0] == "SEMICOLON":
                        self.consume("SEMICOLON")
                    else:
                        raise ParserError("Expected ';' at the end of variable declaration")

                    # Return a VarDeclNode
                    return VarDeclNode(data_type, var_name, value)
                else:
                    raise ParserError("Expected variable name")
            else:
                raise ParserError("Expected data type (e.g., int, float)")
        else:
            raise ParserError("Expected 'FR' for variable declaration")

    def scan_stmt(self):
        """
        Parse an input statement.
        Example: SCAN x;
        """
        if self.current_token[0] == "SCAN":
            self.consume("SCAN")  # Consume 'SCAN'

            # Parse the variable name
            if self.current_token[0] == "IDENTIFIER":
                var_name = self.current_token[1]
                self.consume("IDENTIFIER")

                # Consume the semicolon
                if self.current_token[0] == "SEMICOLON":
                    self.consume("SEMICOLON")
                    return ScanStmtNode(var_name)  # Return a ScanStmtNode
                else:
                    raise ParserError("Expected ';' at the end of input statement")
            else:
                raise ParserError("Expected variable name after 'SCAN'")
        else:
            raise ParserError("Expected 'SCAN'")


    def func_decl(self):
        """
        Parse a function declaration.
        Example: Brew int foo() { ... }
        """
        if self.current_token[0] == "Brew":
            self.consume("Brew")  # Consume 'Brew'

            # Parse the return type
            if self.current_token[0] in ["int", "float", "void"]:
                return_type = self.current_token[0]
                self.consume(return_type)
            else:
                raise ParserError("Expected return type (e.g., int, float)")

            # Parse the function name
            if self.current_token[0] == "IDENTIFIER":
                func_name = self.current_token[1]
                self.consume("IDENTIFIER")
            else:
                raise ParserError("Expected function name")

            # Parse the parameter list
            if self.current_token[0] == "LPAREN":
                self.consume("LPAREN")  # Consume '('
                params = self.param_list()  # Parse the parameter list
                if self.current_token[0] == "RPAREN":
                    self.consume("RPAREN")  # Consume ')'
                else:
                    raise ParserError("Expected ')' after parameter list")
            else:
                raise ParserError("Expected '(' after function name")

            # Parse the function body
            if self.current_token[0] == "LBRACE":
                self.consume("LBRACE")  # Consume '{'
                body = self.block()  # Parse the block of statements
                if self.current_token[0] == "RBRACE":
                    self.consume("RBRACE")  # Consume '}'
                else:
                    raise ParserError("Expected '}' after function body")
            else:
                raise ParserError("Expected '{' to start function body")

            # Return a FuncDeclNode
            return FuncDeclNode(return_type, func_name, params, body)
        
    def if_stmt(self):
        """
        Parse an if statement.
        Example: Lowkey (x < 10) { ... } Else { ... }
        """
        if self.current_token[0] == "Lowkey":
            self.consume("Lowkey")  # Consume 'Lowkey'

            # Parse the condition
            if self.current_token[0] == "LPAREN":
                self.consume("LPAREN")  # Consume '('
                condition = self.expr()  # Parse the condition expression
                if self.current_token[0] == "RPAREN":
                    self.consume("RPAREN")  # Consume ')'
                else:
                    raise ParserError("Expected ')' after condition")
            else:
                raise ParserError("Expected '(' after 'Lowkey'")

            # Parse the 'then' block
            if self.current_token[0] == "LBRACE":
                self.consume("LBRACE")  # Consume '{'
                if_block = self.block()  # Parse the block of statements
                if self.current_token[0] == "RBRACE":
                    self.consume("RBRACE")  # Consume '}'
                else:
                    raise ParserError("Expected '}' after 'then' block")
            else:
                raise ParserError("Expected '{' to start 'then' block")

            # Parse the 'else' block (optional)
            else_block = None
            if self.current_token and self.current_token[0] == "Else":
                self.consume("Else")  # Consume 'Else'
                if self.current_token[0] == "LBRACE":
                    self.consume("LBRACE")  # Consume '{'
                    else_block = self.block()  # Parse the block of statements
                    if self.current_token[0] == "RBRACE":
                        self.consume("RBRACE")  # Consume '}'
                    else:
                        raise ParserError("Expected '}' after 'else' block")
                else:
                    raise ParserError("Expected '{' to start 'else' block")

            # Return an IfNode with the condition, if_block, and else_block
            return IfNode(condition, if_block, else_block)
        else:
            raise ParserError("Expected 'Lowkey' to start an if statement")


    

        
   


        
        
