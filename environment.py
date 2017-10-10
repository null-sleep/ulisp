class Environment():
    def __init__(self, stack=None, fn_parameters=None, fn_args=None):
        self.reference_table = {}
        self.stack = stack or None
        # Assists function calls to set parameters quickly
        if fn_parameters:
            for i in range(len(fn_parameters)):
                self.reference_table[fn_parameters[i]] = fn_args[i]

    def set(self, key, value):
        self.reference_table[key] = value
        # Do I really need a return?
        return value

    def find_reference(self, key):
        if key in self.reference_table:
            return self
        elif self.stack:
            return self.stack.find_reference(key)
        else:
            return None

    def resolve(self, key):
        env = self.find_reference(key)
        if not env:
            raise Exception("Could not resolve reference to {}".format(key))
        return env.reference_table[key]
