class RubitoError(Exception):
    pass 

class NoVariableError(RubitoError):
    pass

class FunctionCallError(RubitoError):
    pass

class RubitoReturn(RubitoError):
    pass

class Scope:
    def __init__(self, variables, up):
        self.variables = variables
        self.up = up

    def __getitem__(self, variable):
        scope = self
        while scope is not None:
            if variable in scope.variables:
                return scope.variables[variable]
            else:
                scope = scope.up
        raise NoVariableError("no variable %s" % variable)

    def __setitem__(self, variable, value):
        self.variables[variable] = value


