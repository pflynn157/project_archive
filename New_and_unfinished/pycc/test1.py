#!/usr/bin/python3

from scanner import Scanner
from ast import *

scan = Scanner("./first.tl")

token = scan.get_next()
while token != "eof":
    if token == "ID":
        print(token + " -> " + scan.get_id_value())
    elif token == "INT":
        print(token + " -> " + str(scan.get_int_value()))
    else:
        print(token)
    token = scan.get_next()
    
##
## Construct a basic AST
##
ast_file = AstFile("first")

prog1 = AstProgram("main")
prog1.return_type = AstInt32Type()
ast_file.functions.append(prog1)

begin = AstBegin()
prog1.block.append(begin)

ret1 = AstReturn()
ret1.expr = AstInt(5)
prog1.block.append(ret1)

##
## Unparse
##
print("-----------------------------")
print(ast_file.unparse())

print("-----------------------------")
#ast_file.set_unparse_language("c++")
ast_file.lang = "c++"
print(ast_file.unparse())

print("-----------------------------")
ast_file.set_unparse_language("ada")
print(ast_file.unparse())

 
