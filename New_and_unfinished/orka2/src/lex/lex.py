##
## This is the configuration file for generating the lexical analyzer.
## The analyzer will end up in the source root of the build directory.
## You will minilex in order to run this.
##

# Define the keywords
keywords = [
    ("extern", "Extern"), ("func", "Func"), ("end", "End"), ("return", "Return"),
    ("struct", "Struct"), ("enum", "Enum"),
    ("var", "VarD"), ("const", "Const"),
    ("bool", "Bool"), ("char", "Char"), ("string", "Str"),
    ("i8", "I8"), ("u8", "U8"), ("i16", "I16"), ("u16", "U16"), 
    ("i32", "I32"), ("u32", "U32"), ("i64", "I64"), ("u64", "U64"),
    ("if", "If"), ("elif", "Elif"), ("else", "Else"), ("while", "While"),
    ("is", "Is"), ("then", "Then"), ("do", "Do"), ("of", "Of"),
    ("break", "Break"), ("continue", "Continue"),
    ("import", "Import"),
    ("true", "True"), ("false", "False"),
    ("and", "Logical_And"), ("or", "Logical_Or")
]

# Define the symbols
symbols = [
    (".", "Dot"), (";", "SemiColon"), (",", "Comma"),
    ("(", "LParen"), (")", "RParen"), ("[", "LBracket"), ("]", "RBracket"),
    ("+", "Plus"), ("-", "Minus"), ("*", "Mul"), ("/", "Div"), ("%", "Mod"),
    ("&", "And"), ("|", "Or"), ("^", "Xor"),
    (":", "Colon"), ("::", "DoubleColon"),
    (">", "GT"), (">=", "GTE"),
    ("<", "LT"), ("<=", "LTE"),
    ("=", "EQ"), ("!=", "NEQ"),
    (":=", "Assign"),
    ("->", "Arrow")
]

# Define single-line comments
single_comments = [ "#" ]

# Define multi-line comments
multi_comments = []

