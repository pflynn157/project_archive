 
class AstNode:
    def __init__(self):
        pass
    
    def unparse(self, lang, indent = ''):
        raise NotImplementedError
    
class AstFile(AstNode):
    languages = [ "default", "c++", "ada" ]
    lang = "default"
    
    functions = list()
    
    def __init__(self, name):
        self.name = name
        
    def set_unparse_language(self, lang):
        if lang not in self.languages:
            print("ERROR: Unknown unparsing language.")
            print("INFO: Defaulting to AST unparsing")
        else:
            self.lang = lang
        
    def unparse(self, indent = ''):
        ret = ""
        for func in self.functions:
            ret += func.unparse(self.lang, '')
        return ret
    
##
## Functions
##
# Base class, don't use directly
class AstFunction(AstNode):
    args = list()
    return_type = None
    block = list()
    
    def __init__(self, name):
        self.name = name
        
    def unparse(self, lang, indent = ''):
        if lang == "c++":
            ret = "{} {}()\n{{\n".format(self.return_type.unparse(lang), self.name);
            for stmt in self.block:
                ret += stmt.unparse(lang, '  ') + "\n"
            ret += "}\n";
            return ret;
        elif lang == "ada":
            ret = ""
            if self.return_type is AstVoidType:
                ret = "procedure {} is\n".format(self.name)
            else:
                ret = "function {} return {} is\n".format(self.name, self.return_type.unparse(lang));
            for stmt in self.block:
                ret += stmt.unparse(lang, '  ') + "\n"
            ret += "end {};\n".format(self.name)
            return ret
        else:
            raise NotImplementedError
    
class AstProgram(AstFunction):
    def unparse(self, lang, indent = ''):
        if lang == "default":
            ret = "program {}() -> {} is\n".format(self.name, self.return_type.unparse(lang))
            for stmt in self.block:
                ret += stmt.unparse(lang, '  ') + "\n"
            ret += "end"
            return ret
        else:
            return super().unparse(lang, indent)
    
##
## Statements
##
class AstStatement(AstNode):
    expr = None
    
    def unparse(self, lang, indent = ''):
        return NotImplementedError
    
class AstBegin(AstStatement):
    def unparse(self, lang, indent = ''):
        if lang == "ada" or lang == "default":
            return "begin"
        else:
            return ";"
    
class AstReturn(AstStatement):
    def unparse(self, lang, indent = ''):
        if self.expr is not None:
            return "{}return {};".format(indent, self.expr.unparse(lang))
        else:
            return "{}return;".format(indent)
    
##
## Expressions
##
class AstExpression(AstNode):
    def unparse(self, lang, indent = ''):
        return NotImplementedError
    
class AstInt(AstExpression):
    value = 0
    
    def __init__(self, value):
        self.value = value
    
    def unparse(self, lang, indent = ''):
        return str(self.value)

##
## Data types
##
class AstDataType(AstNode):
    def unparse(self, lang, indent = ''):
        return NotImplementedError
    
class AstVoidType(AstDataType):
    def unparse(self, lang, indent = ''):
        return NotImplementedError
    
class AstInt8Type(AstDataType):
    def unparse(self, lang, indent = ''):
        return NotImplementedError
    
class AstInt16Type(AstDataType):
    def unparse(self, lang, indent = ''):
        return NotImplementedError
    
class AstInt32Type(AstDataType):
    def unparse(self, lang, indent = ''):
        if lang == "c++":
            return "int"
        elif lang == "ada":
            return "integer"
        else:
            return "i32"
    
class AstInt64Type(AstDataType):
    def unparse(self, lang, indent = ''):
        return NotImplementedError
    
