"""
Rubito interpreter
__author__      = Rubito team
__version__     = 0.1
"""

from rubito.scope import *
from rubito.robject import *

BUILTIN = Scope(variables={}, up=None)
OPERATORS = {
    '==': lambda l, r: RBool(l.value == r.value),
    '-':  lambda l, r: RNumber(l.value - r.value),
    '*':  lambda l, r: RNumber(l.value * r.value)
}
    

class Interpreter:
    def __init__(self, ast):
        self.ast = ast

    def eval(self):
        return self.eval_node(self.ast, BUILTIN)

    def eval_node(self, node, scope):
        name = 'eval_%s' % node.rule_name
        # print(name, node)
        if hasattr(node, '__iter__'):
            return getattr(self, name)(*node, scope=scope)
        else:
            return getattr(self, name)(node, scope=scope)

    def eval_program(self, *codes, scope):
        return [self.eval_node(code, scope) for code in codes][-1]

    def eval_toplevel(self, code, scope):
        return self.eval_node(code, scope)

    def eval_function(self, _, name, args, body, scope):
        arg_names = [arg.value for arg in args[1:-1]]
        f = RFunction(name.value, arg_names, body)
        scope[name.value] = f
        return f

    def eval_functioncall(self,call, _paren, params, _rparen, scope):
        q = scope[call.value]
        if len(q.args) != len(params):
            raise FunctionCallError("expected %d args" % len(params))

        args = {arg: self.eval_node(param, scope) for arg, param in zip(q.args, params)}
        function_scope = Scope(args, scope)

        try:
            result = self.eval_node(q.body, scope=function_scope)[-1]
        except RubitoReturn as e:
            result = function_scope['_return']
        # print('RETURN %s %s' % (call.value, result))
        return result

    def eval_expression(self, code, scope):
        return self.eval_node(code, scope)

    def eval_block(self, _paren, *codes, _rparen=')', scope=None):
        return [self.eval_node(a, scope) for a in codes[:-1]]

    def eval_statement(self, *code, scope=None):
        return self.eval_node(code[0], scope)

    def eval_ifstatement(self, _, _paren, test, _rparen, if_branch, _else, else_branch, scope=None):
        t = self.eval_node(test, scope)
        if t.value:
            return self.eval_node(if_branch, scope)
        else:
            return self.eval_node(else_branch, scope)

    def eval_operation(self, left, operator, right, scope):
        l, r = self.eval_node(left, scope), self.eval_node(right, scope)
        # print(l, r)
        return OPERATORS[operator.value](l, r)

    def eval_symbol(self, name, scope):
        return scope[name.value]

    def eval_returnstatement(self, _, expression, scope):
        scope['_return'] = self.eval_node(expression, scope)
        raise RubitoReturn("return")

    def eval_literal(self, a, scope):
        if a.value.isdigit():
            return RNumber(int(a.value))
        elif isinstance(a.value, str):
            return RString(a.value)
        else:
            raise NotImplementedError(str(a.value))
