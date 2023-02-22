
##
## The main class for the scanner
##
class Scanner:
    ##
    ## Class-level variables
    ##
    content = list()
    index = 0
    buf = ""
    stack = list()
    id_val = ""
    
    keywords = [
        "program", "is", "end",
        "return",
        "i32"
    ]
    
    symbols = [ ';', '(', ')', '->' ]
    
    ##
    ## Functions
    ##
    def __init__(self, input_file):
        with open(input_file, "r") as reader:
            self.content += reader.read()
    
    def get_next(self):
        if len(self.stack) > 0:
            return self.stack.pop()
        
        if self.index >= len(self.content):
            return "eof"
        
        while self.index < len(self.content):
            c = self.content[self.index]
            if c == ' ' or c == '\n' or c in self.symbols:
                self.index += 1
                if c in self.symbols:
                    if len(self.buf) == 0:
                        return str(c)
                    else:
                        self.stack.append(str(c))
                
                if len(self.buf) == 0:
                    continue
                
                if self.buf in self.symbols:
                    token = self.buf
                elif self.buf in self.keywords:
                    token = self.buf
                else:
                    try:
                        tst = int(self.buf)
                        token = "INT"
                    except:
                        token = "ID"
                    self.id_val = self.buf
                self.buf = ""
                return token
            else:
                self.buf += c
                self.index += 1
                
        return "eof"
    
    def get_id_value(self):
        return self.id_val
    
    def get_int_value(self):
        return int(self.id_val)
    
