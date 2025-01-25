from lexer import Lexer
import parser as pr
from ast_nodes import VarDeclNode, VarUseNode, ExprNode, PrintNode

# Define the SymbolTable class
class SymbolTable:
    def __init__(self):
        self.table = {}

    def add_symbol(self, var_name, data_type):
        if var_name in self.table:
            raise Exception(f"Variable '{var_name}' already declared!")
        self.table[var_name] = data_type

    def get_symbol(self, var_name):
        if var_name not in self.table:
            raise Exception(f"Variable '{var_name}' is not declared!")
        return self.table[var_name]

# Define the SemanticChecker class
class SemanticChecker:
    def __init__(self):
        self.symbol_table = SymbolTable()

    def check(self, ast):
        for node in ast:
            self.visit(node)

    def visit(self, node):
        if isinstance(node, pr.VarDeclNode):  # Variable Declaration
            self.symbol_table.add_symbol(node.var_name, node.data_type)
        elif isinstance(node, pr.VarUseNode):  # Variable Usage
            self.symbol_table.get_symbol(node.var_name)
        elif isinstance(node, pr.ExprNode):  # Expressions
            self.check_expr(node)

    def check_expr(self, node):
        # Add type checking logic for expressions if required
        pass

# Define the CodeGenerator class
class CodeGenerator:
    def __init__(self):
        self.code = []
        self.temp_counter = 1  # For generating temporary variable names like t1, t2, etc.
        self.label_counter = 1  # For generating unique labels for if-else conditions

    def generate(self, ast):
        for node in ast:
            self.visit(node)

    def visit(self, node):
        print(f"Visiting node: {type(node)}")  # Debugging line to print node type

        if isinstance(node, pr.PrintNode):
            # Print statement in 3AC
            if isinstance(node.expr, pr.StringNode):
            # Handle case when the expression is a string literal
                expr_code = f'"{node.expr.value}"'  # Directly use the string value
            else:
            # Handle case when the expression is an actual expression (ExprNode)
                expr_code = self.visit(node.expr)  # Recursively visit the expression node

            # Append the generated print code to the code list
            self.code.append(f"print {expr_code}")
        elif isinstance(node, pr.StringNode):
            return f'"{node.value}"'

        elif isinstance(node, pr.VarDeclNode):
            # Variable declaration in 3AC
            temp_var = f"t{self.temp_counter}"
            self.temp_counter += 1
            expr_code = self.visit(node.expr)
            self.code.append(f"{temp_var} = {expr_code}")
            self.code.append(f"{node.var_name} = {temp_var}")

        elif isinstance(node, pr.NumberNode):
            # Return the number value in 3AC
            return node.value

        elif isinstance(node, pr.IdentifierNode):
            # Return the identifier in 3AC
            return node.name

        elif isinstance(node, pr.AddNode):
            # Arithmetic addition: t1 = t2 + t3
            left_code = self.visit(node.left)
            right_code = self.visit(node.right)
            temp_var = f"t{self.temp_counter}"
            self.temp_counter += 1
            self.code.append(f"{temp_var} = {left_code} + {right_code}")
            return temp_var

        elif isinstance(node, pr.SubNode):
            # Arithmetic subtraction: t1 = t2 - t3
            left_code = self.visit(node.left)
            right_code = self.visit(node.right)
            temp_var = f"t{self.temp_counter}"
            self.temp_counter += 1
            self.code.append(f"{temp_var} = {left_code} - {right_code}")
            return temp_var

        elif isinstance(node, pr.MulNode):
            # Arithmetic multiplication: t1 = t2 * t3
            left_code = self.visit(node.left)
            right_code = self.visit(node.right)
            temp_var = f"t{self.temp_counter}"
            self.temp_counter += 1
            self.code.append(f"{temp_var} = {left_code} * {right_code}")
            return temp_var

        elif isinstance(node, pr.DivNode):
            # Arithmetic division: t1 = t2 / t3
            left_code = self.visit(node.left)
            right_code = self.visit(node.right)
            temp_var = f"t{self.temp_counter}"
            self.temp_counter += 1
            self.code.append(f"{temp_var} = {left_code} / {right_code}")
            return temp_var

        elif isinstance(node, pr.ModNode):
            # Arithmetic modulus: t1 = t2 % t3
            left_code = self.visit(node.left)
            right_code = self.visit(node.right)
            temp_var = f"t{self.temp_counter}"
            self.temp_counter += 1
            self.code.append(f"{temp_var} = {left_code} % {right_code}")
            return temp_var

        elif isinstance(node, pr.IfNode):
            # If-Else condition handling
            cond_code = self.visit(node.condition)
            true_label = f"label{self.label_counter}"
            false_label = f"label{self.label_counter + 1}"
            self.label_counter += 2

            self.code.append(f"if {cond_code} goto {true_label}")
            self.code.append(f"goto {false_label}")
            self.code.append(f"{true_label}:")
            # Process the true block
            for stmt in node.true_block:
                self.visit(stmt)
            self.code.append(f"goto end_if_{self.label_counter}")

            self.code.append(f"{false_label}:")
            # Process the false block
            for stmt in node.false_block:
                self.visit(stmt)

            self.code.append(f"end_if_{self.label_counter}:")

# Example usage:
lexer = Lexer("FR int wtl_x=7;")
tokens = lexer.tokenize()
print(tokens)


try:
    parser = pr.Parser(tokens)
    print("Parsing tokens...")
    ast = parser.parse()
    print("AST generated successfully:")
    for node in ast:
        print(type(node), node.__dict__)
except Exception as e:
    print("Error during parsing:", e)
    raise

try:
    print("Running semantic checks...")
    semantic_checker = SemanticChecker()
    semantic_checker.check(ast)
    print("Semantic analysis completed successfully.")
except Exception as e:
    print("Error during semantic analysis:", e)
    raise

try:
    print("Generating 3AC code...")
    code_generator = CodeGenerator()
    code_generator.generate(ast)
    print("Generated 3AC Code:")
    print("\n".join(code_generator.code))
except Exception as e:
    print("Error during code generation:", e)
    raise

""" parser = pr.Parser(tokens)
ast = parser.parse()

semantic_checker = SemanticChecker()
semantic_checker.check(ast)

print("Tokens:", tokens)
print("AST Generated:", ast)
print("AST nodes:")
for node in ast:
    print(type(node), node.__dict__)

code_generator = CodeGenerator()
code_generator.generate(ast)
print("\nGenerated 3AC Code:")
print("\n".join(code_generator.code))
 """