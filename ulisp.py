import sys
import read
import utypes
import signal
import utypes
import traceback
import ulispreadline
from namespace import ns
from environment import Environment

# Set recursion depth limit
sys.setrecursionlimit(1500)
# Flag for Ctrl+C exit
EXIT = False

def sigint_handler(signum, frame):
    """Handels program exit with Ctrl+C"""
    global EXIT
    if EXIT:
        sys.exit()
    else:
        print("\nPress CTRL+C again, to exit")
        EXIT = True

signal.signal(signal.SIGINT, sigint_handler)


def eval_ast(ast, env):
    if type(ast) == utypes.Symbol:
        #print(ast)
        return env.resolve(ast)
    if type(ast) == utypes.List:
        return utypes.List( map( lambda e: evaluate(e, env), ast) )
    if type(ast) == utypes.Hash:
        # Key is enforced to be String during creation
        key_val_list = utypes.List()
        for key in ast.keys():
            key_val_list.append(evaluate(key, env))
            key_val_list.append(evaluate(ast[key], env))
        return utypes._make_hash(key_val_list)
    # Return primitive type
    else:
        return ast

def evaluate(ast, env):
    while True:
        if not type(ast) == utypes.List:
            return eval_ast(ast, env)
        # the ast in an empty list
        if len(ast) == 0:
            return ast
        first_element = ast[0]

        # Variable definition
        if first_element == 'define':
            if len(ast) == 3:
                if type(ast[1]) == utypes.Symbol:
                    reference_name = ast[1] # variable name
                    result_obj = evaluate(ast[2], env) # variable value
                    return env.set(reference_name, result_obj)
                else:
                    raise Exception('Reference name should be symbol, given {}'.format(type(ast[1])))
            else:
                raise Exception('Invalid number of arguments provided')
        # maybe add case for list declaration without keyword?
        elif first_element == "lambda":
            if len(ast) == 3:
                params = ast[1]
                body = ast[2]
                return utypes._lambda(body, params, env, evaluate, Environment)
            else:
                raise Exception('Invalid number of arguments provided: {}'.format(len(ast)))
        elif first_element == "if":
            condition = evaluate(ast[1], env)
            expression = ast[2]
            if condition in [False, None]:
                if len(ast) == 4:
                    ast = ast[3] # TCO
            else:
                ast = expression # TCO
        elif first_element == "cond":
            for case in ast[1:]:
                if len(case) == 2:
                    condition = evaluate(case[0], env)
                    expression = case[1]
                    if condition not in [False, None]:
                        ast = expression # TCO
                elif len(case) == 1:
                    return evaluate(case[0], env) # TCO
                elif len(case) > 2:
                    raise Exception("More than 3 parameters provided for case")
            return None
        else:
            # We have a function!, aren't s-expressions nice?
            expression = eval_ast(ast, env)
            function = expression[0]
            # We can only optimize user defined functions
            # They can be uniquely identified using the __ast__ attribute
            
            if hasattr(function, '__ast__'):
                ast = function.__ast__
                env = function.__gen_env__(expression[1:])
                #print(type(env))
            else:
                return function(*expression[1:])
        
        # If we have reached here, we dont know how to evaluate provided AST
        #raise Exception('Unknown type evaluated: {}\nAST: {}'.format(type(ast), ast))

# Initialize environment with core language
base_env = Environment()
for key in ns.keys():
    base_env.set(key, ns[key])


# For the lack of a better name
print("Unknown Lisp Version 0.0.1 - Dhruv Jauhar")
while True:
    try:
        line = ulispreadline.readline()
        # reset flag
        EXIT = False
        if line in ["(exit)", "exit", None]: # Add EOF 
            break
        if line == "":
            continue
        # Tranform inpu to abstract syntax tree
        ast = read.read_line(line)
        #print("AST: " + str(ast))
        print(evaluate(ast, base_env))
    except Exception as e:
        print("An unknown exception has occured")
        print("".join(traceback.format_exception(*sys.exc_info())))
