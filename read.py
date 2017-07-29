import re



def tokenize(line):
    exp = re.compile(r"""[\s,]*(~@|[\[\]{}()'`~^@]|"(?:[\\].|[^\\"])*"?|;.*|[^\s\[\]{}()'"`@,;]+)""")
    return [t for t in re.findall(exp, str) if t[0] != ';']
