class RObject:
    def __str__(self):
        return repr(self)

class RNumber(RObject):
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return 'number<(%s)>' % self.value

class RString(RObject):
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return 'string<(\"%s\")>' % self.value

class RFunction(RObject):
    def __init__(self, name, args, body):
        self.name = name
        self.args = args
        self.body = body

    def __repr__(self):
        return 'function<%s(%s)>' % (self.name, ','.join(self.args))


class RBool(RObject):
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return repr(self.value)
