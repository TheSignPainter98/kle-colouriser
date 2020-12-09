from .util import dict_union
from .yaml_io import read_yaml
from collections import OrderedDict
from pyparsing import infixNotation, Literal, oneOf, opAssoc, ParserElement, ParseException, pyparsing_common, Word
from sys import getrecursionlimit, setrecursionlimit
from typing import Callable, Iterator, List, Tuple

LOWER_RECURSION_LIMIT:int = 3000

uniops:OrderedDict = OrderedDict([
        ('+', lambda v: v),
        ('-', lambda v: -v),
    ])
binops:OrderedDict = OrderedDict([
        ('^', lambda a,b: a ** b),
        ('*', lambda a,b: a * b),
        ('/', lambda a,b: a / b),
        ('//', lambda a,b: a // b),
        ('+', lambda a,b: a + b),
        ('-', lambda a,b: a - b),
    ])
condops:OrderedDict = OrderedDict([
        ('<', lambda a,b: a < b),
        ('<=', lambda a,b: a <= b),
        ('>', lambda a,b: a > b),
        ('>=', lambda a,b: a >= b),
        ('=', lambda a,b: a == b),
        ('==', lambda a,b: a == b),
        ('!=', lambda a,b: a != b),
    ])
ops = dict_union(uniops, binops, condops)

def parse_colour_map(fname:str) -> [dict]:
    raw_map:[dict] = read_yaml(fname)
    colour_map:[dict] = list(map(parse_equations, raw_map))
    return colour_map

def parse_equations(rule:dict) -> dict:
    return recursively_add(rule, 'key-pos', 'parsed-key-pos', parse_equation)

def parse_equation(eq:str) -> dict:
    ParserElement.enablePackrat()

    if getrecursionlimit() <= LOWER_RECURSION_LIMIT:
        setrecursionlimit(LOWER_RECURSION_LIMIT)

    # Define atoms
    NUM = pyparsing_common.number
    VARIABLE = Word(['x', 'y'], exact=True)
    operand = NUM | VARIABLE

    # Define production rules
    expr = infixNotation(operand,
            [ (Literal(op), 1, opAssoc.RIGHT, op_rep) for op in uniops ]
            + [ (Literal(op), 2, opAssoc.LEFT, op_rep) for op in binops ]
        )
    cond = infixNotation(expr,
            [ (Literal(op), 2, opAssoc.LEFT, op_rep) for op in condops ]
        )

    try:
        return cond.parseString(eq, parseAll=True)[0]
    except ParseException as pex:
        print('Error while parsing "%s": %s' %(eq, str(pex)))
        return None

def op_rep(_1:str, _2:int, toks:List[object]) -> dict:
    toks = toks[0]
    op:str
    op_args:[object]
    if len(toks) == 2:
        op = toks[0]
        op_args = [toks[1]]
    elif len(toks) == 3:
        op = toks[1]
        op_args = [toks[0], toks[2]]
    else:
        print('Unknown number of tokens: %d in %s' %(len(toks), list(map(str, toks))))
        exit(1)
    return {
        'op': ops[op],
        'pretty-op': op,
        'args': op_args,
    }

def recursively_add(data:object, old_key:str, new_key:str, f:Callable) -> object:
    rules:dict = {
        dict: lambda d: dict_union({ k: (recursively_add(v, old_key, new_key, f) if k != old_key else v) for k,v in d.items() }, { new_key: f(d[old_key]) } if old_key in d else {}),
        float: lambda f: f,
        int: lambda i: i,
        list: lambda l: list(map(lambda e: recursively_add(e, old_key, new_key, f), data)),
        str: lambda s: s,
        type(None): lambda n: n,
    }
    return rules[type(data)](data)
