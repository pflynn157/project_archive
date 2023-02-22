#!/usr/bin/python3

from parser import Parser
from ast import *

builder = Parser("./first.tl")
builder.parse()
ast = builder.get_ast()

print(ast.unparse())
