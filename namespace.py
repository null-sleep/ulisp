from math import *
from utypes import *
from fractions import gcd
from functools import reduce

def signum(num):
    if num == 0:
        return 0
    elif num > 0:
        return 1
    else:
        return -1

def n_gcd(*numbers):
    return reduce(gcd, numbers)

def lcm(*numbers):  
    def lcm(a, b):
        return (a * b) // gcd(a, b)
    return reduce(lcm, numbers, 1)

def sum(*args):
    total = 0
    for i in args:
        total += i
    return total

def difference(*args):
    first = args[0]
    for i in args[1:]:
        first -= i
    return first

def product(*args):
    total = 1
    for i in args:
        total *= i
    return total

def n_list(*args):
    return List(args)

ns ={
    # Core
    'none': None,
    'eq?': lambda a,b: a == b,
    'none?': lambda x: True if x == None else False,
    'true?': lambda x: bool(x)  ,
    'false?': lambda  x: not bool(x),
    'boolean?': lambda x: type(x) == bool,
    'symbol': None,
    'symbol?': lambda x: type(x) == Symbol,
    'keyword?': None,
    'atom?': lambda x: type(x) in [Symbol, True, False, int, float, None, String],
    'print': None, # gve __repr__ output
    'time': lambda : int(time.time() * 1000), # in ms

    # String
    'string?': lambda x: type(x) == String,

    # List
    'list': n_list,
    'list?': lambda x: type(x) == List,
    'cons': lambda val, lst: List([val]) if lst == None else List([x]) + lst,
    'first': lambda lst: lst[0] if len(lst) > 0 else None,
    'second': lambda lst: lst[1] if len(lst) > 1 else None,
    'rest': lambda lst: lst[1:] if len(lst) > 0 else None,
    'nth': lambda lst, index: lst[index] if len(lst) > index - 1 else None,
    'empty?': lambda lst: bool(len(lst)),
    'count': lambda lst: len(lst),
    'map': lambda func, lst: List(map(func, lst)),
    'filter': lambda func, lst: List(filter(func, lst)),
    'reduce': lambda func, lst: List(reduce(func, lst)), # func must take 2 args

    # Hash
    'hash?': lambda x: type(x) == Hash,
    'get': lambda hashmap, index: hashmap[index],
    'keys': lambda hashmap: List(hashmap.keys),
    'vals': lambda hashmap: List(hashmap.values),
    'contains?': lambda hashmap, index: lambda hashmap, index: True if hashmap.get(index) else False,
    
    # Math
    'integer?': lambda x: type(x) == int,
    'float?': lambda x: type(x) == float,
    '=': lambda a,b: a == b,
    '!=': lambda a,b: a != b,
    '>=': lambda a,b: a >= b,
    '<=': lambda a,b: a <= b,
    '>': lambda a,b: a > b,
    '<': lambda a,b: a < b,
    '+': sum,
    '-': difference,
    '*': product,
    '/': lambda a,b: a / b,
    '%': lambda a,b: a % b,
    'abs': abs,
    'add1': lambda x: x + 1,
    'sub1': lambda x: x - 1,
    'max': max,
    'min': min,
    'gcd': n_gcd,
    'lcm': lcm,
    'round': round,
    'floor': floor,
    'ceil': ceil,
    'quotient': lambda a,b: floor(a / b),
    'remainder': lambda a,b: a % b,
    'modulo': lambda a,b: a % b,
    'exp': exp, # e^input
    'expt': lambda a,b: a ** b, # args: o t gives o^t
    'sqr': lambda x: x * x,
    'sqrt': sqrt,
    'sgn': signum,
    'sin': sin,
    'cos': cos,
    'tan': tan,
    'asin': asin,
    'acos': acos,
    'atan': atan,
    'random': None, #https://docs.racket-lang.org/reference/generic-numbers.html#%28part._.Powers_and_.Roots%29
    'number->string': lambda x: String(x), 
    'string->number': lambda x: float(x) if '.' in x else int(x),
    'pi': 3.141592653589793,


}