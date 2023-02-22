from scanner import Scanner
from ast import *

class Parser:
    def __init__(self, input_file):
        self.scanner = Scanner(input_file)
        self.ast = AstFile(input_file)
    
    def get_ast(self):
        return self.ast
    
    def parse(self):
        token = self.scanner.get_next()
        while token != "eof":
            if token == "program":
                self.parse_function(token)
            else:
                print("ERROR: Unknown token in the global scope.")
                print(" --> " + str(token))
            token = self.scanner.get_next()
            
    ##
    ## Builds a function of some kind
    ##
    def parse_function(self, start_token):
        token = self.scanner.get_next()
        name = self.scanner.get_id_value()
        if token != "ID":
            print("ERROR: Expected function name.")
            print(" --> " + str(token))
            return
        
        # Next token should be arguments
        token = self.scanner.get_next()
        if token != "(":
            print("ERROR: Expected function arguments list.")
            print(" --> " + str(token))
            return
        while token != ")" and token != "eof":
            token = self.scanner.get_next()
            
        # Next token should be arrow
        token = self.scanner.get_next()
        if token != "->":
            print("ERROR: Expected \"->\" before data type indication.")
            print(" --> " + str(token))
            return
        
        # Next token should be data type
        data_type = self.parse_data_type()
        
        # Final token should be is
        token = self.scanner.get_next()
        if token != "is":
            print("ERROR: Expected \"is\" before block.")
            print(" --> " + str(token))
            return
        
        # Build the AST node
        # TODO: Check
        func = AstProgram(name)
        func.return_type = data_type
        self.ast.functions.append(func)
        
        # Build the block
        self.parse_block(func, func)
        
    ##
    ## Parses a statement block
    ##
    def parse_block(self, parent, parent_type):
        token = self.scanner.get_next()
        while token != "end" and token != "eof":
            if token == "return":
                node = AstReturn()
                node.expr = self.parse_expression(";")
                parent.block.append(node)
            else:
                print("ERROR: Unexpected token in block.")
                print(" --> " + str(token))
                return
            token = self.scanner.get_next()
            
    ##
    ## Parses an expression
    ##
    def parse_expression(self, stop_token):
        output = list()
        
        token = self.scanner.get_next()
        while token != stop_token and token != "eof":
            if token == "INT":
                output.append(AstInt(self.scanner.get_int_value()))
            else:
                print("ERROR: Unexpected token in expression.")
                print(" --> " + str(token))
                return None
            token = self.scanner.get_next()
            
        if len(output) >= 1:
            return output.pop()
        return None
        
    ##
    ## Parses a data type
    ##
    def parse_data_type(self):
        token = self.scanner.get_next()
        if token == "void":
            return AstVoidType()
        elif token == "char":
            return AstCharType()
        elif token == "bool":
            return AstBoolType()
        elif token == "i8" or token == "u8":
            return AstInt8Type()
        elif token == "i16" or token == "u16":
            return AstInt16Type()
        elif token == "i32" or token == "u32":
            return AstInt32Type()
        elif token == "i64" or token == "u64":
            return AstInt64Type()
        elif token == "string":
            return AstStringType()
        else:
            print("ERROR: Expected data type.")
            print(" --> " + str(token))
        return AstVoidType()
    
