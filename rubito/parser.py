"""
Rubito parser
__author__      = Rubito team
__version__     = 0.1
"""

from arpeggio import *
from arpeggio import RegExMatch as _


def comment():
    return [_("//.*"), _("/\*.*\*/"), _("\#.*"), _("#\*.*\*/")]


def literal():
    return _(r'\d*\.\d*|\d+|".*?"')


def symbol():
    return _(r"\w+")


def operator():
    return _(r"\+|\-|\*|\/|\=\=")


def operation():
    return symbol, operator, [literal, functioncall]


def expression():
    return [literal, operation, functioncall]


def expressionlist():
    return expression, ZeroOrMore(",", expression)


def returnstatement():
    return Kwd("return"), expression


def ifstatement():
    return Kwd("if"), "(", expression, ")", block, Kwd("else"), block


def statement():
    return [ifstatement, returnstatement], ";"


def block():
    return Kwd("do"), OneOrMore(statement), Kwd("end")


def parameterlist():
    return "(", symbol, ZeroOrMore(",", symbol), ")"


def functioncall():
    return symbol, "(", expressionlist, ")"


def function():
    return Kwd("fn"), symbol, parameterlist, block

def program():
    return OneOrMore(toplevel)

def toplevel():
    return [functioncall, function]

def parse(source, debug=True):
    return ParserPython(program, comment, debug=debug).parse(source)
