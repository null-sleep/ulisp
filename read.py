import re
from utypes import List, Hash, String, Symbol, Quote, _make_hash

REGEX_TOKENIZE_EXP = r"""[\s,]*(~@|[\[\]{}()'`~^@]|"(?:[\\].|[^\\"])*"?|;.*|[^\s\[\]{}()'"`@,;]+)"""

def tokenize(str):
    # Compiles only once, on first function call
    tokenize.tre = re.compile(REGEX_TOKENIZE_EXP)
    return [t for t in re.findall(tokenize.tre, str) if t[0] != ';']


class TokenStream():
    def __init__(self, tokens, position =0):
        self.tokens = tokens
        self.position = position
        self.token_count = len(tokens)

    def peek(self):
        if self.position < self.token_count:
            return self.tokens[self.position]
        else:
            return None

    def next(self):
        self.position += 1
        return self.tokens[self.position - 1]

   
def read_list(ts):
    ast = List()
    token = ts.next()
    if token not in ["(", "["]:
        pass # mismatched ()
    token = ts.peek()
    while token not in [")", "]"]:
        pass # syntax error, mismatched brackets
        ast.append(form_ast(ts))
        token = ts.peek()
    ts.next()
    return ast


def read_hash_map(ts):
    ast = list()
    token = ts.next()
    if token != "{":
        pass # mismatched ()
    token = ts.peek()
    while token != "}":
        pass # syntax error, mismatched brackets
        ast.append(form_ast(ts))
        token = ts.peek()
    ts.next()
    if len(ast) % 2 != 0:
        pass # Raise exception, missing value for key, count mismatch
    return _make_hash(ast)


def read_atom(ts):
    token = ts.next()
    # empty, True, False are their own types, not symbols
    if token == "empty":
        return None
    elif token == "true":
        return True
    elif token == "false":
        return False
    elif token.isdigit():
        return int(token)
    elif len(token.split('.')) == 2 and token.split('.')[0].isdigit() and token.split('.')[1].isdigit(): 
        return float(token)
    elif token[0] == '"':
        if token[-1] == '"':
            return str(token[1:-1])
        else:
            pass # raise invalid string exception or something
    else:
        # Defualt symbol type is reference.
        return Symbol(token)


def form_ast(ts):
    token = ts.peek()
    #print(token)
    if token == None:
        return ''
    if token[0] == ';':
        pass # Rasie not implemented error
    elif token == "`":
        ts.next()
        return Quote(form_ast(ts))
        # Add type symbol and evaluate the rest as AST, ready to go
    elif token == "~":
        ts.next
        return Symbol(form_ast(ts))
    elif token in [")", "]"]:
        raise Exception("unexpected ')'")
        pass # Raise bracket mismatch error
    elif token in ["(", "["]:
        return read_list(ts)
    elif token == "}":
        pass # Raise bracket mismatch error
    elif token == "{":
        return read_hash_map(ts)
    else:
        return read_atom(ts) # Must be an atom or could no resolve variable reference


def read_line(line):
    tokens = tokenize(line)
    #print(tokens)
    ts = TokenStream(tokens)
    return form_ast(ts)