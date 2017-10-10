import re

class List(list):
    def __repr__(self):
        exrep = str()
        for item in self.__iter__():
            exrep += "{}, ".format(item)
        return "(" + exrep[:-2] + ")"


class String(str):
    pass


class Hash(dict):
    def __setitem__(self, k, v):
        """Raises an exception if key is repeated during definition"""
        if k in self.keys():
            raise ValueError("Key is already present") # Make into a Syntax error??
        else:
            return super(Hash, self).__setitem__(k, v)

def _make_hash(key_value_pair_list):
    # Resolves list of key-value pairs into a dictionary
    hash_map = Hash()
    for i in range(0, len(key_value_pair_list), 2):
        if type(key_value_pair_list[i]) in [String, Symbol, str]:
            hash_map[key_value_pair_list[i]] = key_value_pair_list[i+1]
        else:
            raise Exception('Invalid key: {} provided'.format(key_value_pair_list[i]))
    return hash_map


class Symbol(str):
    def __repr__(self):
        value = self.__str__()
        return "Symbol<{}> ".format(value)

def _make_symbol(symbol_type, value):
    return Symbol(symbol_type, value)


class Quote():
    def __init__(self, value):
        self.value = value
    def __repr__(self):
        value = str(self.value)
        return "Quote({})".format(value )# Behaves similar to a string


def _lambda(ast, params, env, Eval, Env):
    # ast is the ast of the body of the function
        def function(*args):
            return Eval(ast, Env(env, params, List(args)))
        function.__meta__ = None
        function.__ast__ = ast
        # resolution of args to list handled in function call
        function.__gen_env__ = lambda args: Env(env, params, args)
        return function
