import celexer
tokens = celexer.tokens

from ply import yacc

from ast import *

tokenlist = []
preclist = []

emit_code = 1


def p_literal_list(p):
    '''list : LBRACE RBRACE
            | LBRACE listitems RBRACE'''
    p[0] = List(elts=[] if len(p) == 3 else p[2], ctx=Load())


def p_literal_list_items(p):
    '''listitems : listitems COMMA literal
                 | literal'''
    p[0] = [p[1]] if len(p) == 2 else p[1] + [p[3]]
                 

def p_literal_dict(p):
    '''dict : LBRACKET RBRACKET
            | LBRACKET dictitems RBRACKET'''
    p[0] = Dict(keys=[] if len(p) == 3 else [i[0] for i in p[2]],
                values=[] if len(p) == 3 else [i[1] for i in p[2]])


def p_literal_dict_items(p):
    '''dictitems : dictitems COMMA dictitem
                 | dictitem'''
    p[0] = [p[1]] if len(p) == 2 else p[1] + [p[3]]


def p_literal_dict_item(p):
    '''dictitem : literal COLON literal'''
    p[0] = [p[1], p[3]]


def p_literal_tuple(p):
    '''tuple : LPAREN RPAREN
             | LPAREN tupleitems RPAREN'''
    p[0] = Tuple(elts=[] if len(p) == 3 else p[2], ctx=Load())


def p_literal_tuple_items(p):
    '''tupleitems : tupleitems COMMA literal
                  | literal'''
    p[0] = [p[1]] if len(p) == 2 else p[1] + [p[3]]


def p_literal_call(p):
    '''call : ID LPAREN RPAREN
            | ID LPAREN args RPAREN
            | ID LPAREN args COMMA kwargs RPAREN'''
    p[0] = Call(func=Name(id=p[1], ctx=Load()), args=[] if len(p) == 4 else p[3], keywords=[] if len(p) == 4 else p[5])
    

def p_literal_call_args(p):
    '''args : args COMMA literal
            | literal
            | '*' id
            | '*' list'''
    p[0] = [p[1]] if len(p) == 2 else p[1] + [p[3]] if p[1] != '*' else [p[2]]


def p_literal_call_kwargs(p):
    '''kwargs : kwargs COMMA kwarg
              | kwarg'''
    p[0] = [p[1]] if len(p) == 2 else p[1] + [p[3]]


def p_literal_call_kwarg(p):
    '''kwarg : ID EQ literal
             | '*' '*' id
             | '*' '*' dict'''
    p[0] = keyword(arg=p[1], value=p[3]) if p[1] != '*' else keyword(value=p[3])


def p_id(p):
    '''id : ID'''
    p[0] = Name(id=p[1], ctx=Load())


def p_constant_integer(p):
    '''constant : INTEGER'''
    p[0] = Constant(value=int(p[1]))


def p_constant_float(p):
    '''constant : FLOAT'''
    p[0] = Constant(value=float(p[1]))
    

def p_constant_string(p):
    '''constant : STRING'''
    p[0] = Constant(value=p[1])


def p_constant_boolean(p):
    '''constant : BOOLEAN'''
    p[0] = Constant(value=bool(p[1]))


def p_literal(p):  # function call (returned value), number, string, list, etc
    '''literal : constant
               | NONE
               | call
               | list
               | dict
               | tuple
               | id'''
    p[0] = p[1]


class AssignTemp:
    def __init__(self, targets: list, value):
        self.targets = targets
        self.value = value


def p_subtitute(p):
    '''subtitute : ID EQ literal'''
    p[0] = AssignTemp(targets=[Name(id=p[1], ctx=Store())], value=p[3])


def p_annotation(p):
    '''annotation : ANNOINTEGER
                  | ANNOFLOAT
                  | ANNOSTRING
                  | ANNOBOOLEAN
                  | ANNOLIST
                  | ANNOTUPLE
                  | ANNODICTIONARY
                  | ANNOCALLABLE
                  | ID'''
    p[0] = Name(id=p[1], ctx=Load())


def p_var_init_withdefault(p):
    '''substitute : VAR '<' annotation '>' subtitute'''
    p[0] = AnnAssign(target=Name(id=p[5], ctx=Store()), annotation=p[3], value=p[7])
        
def p_var_init(p):
    '''substitute : VAR '<' annotation '>' ID'''
    p[0] = AnnAssign(target=Name(id=p[5], ctx=Store()), annotation=p[3], value=None)

def p_func_init(p):
    "com : FUNCTION ID '(' call ')'"
    p[0] = FunctionDef(name='func',args=arguments(posonlyargs=[],args=[arg(arg=p[4])],kwonlyargs=[],kw_defaults=[],defaults=[]),body=[Pass()],decorator_list=[])

def p_term_calc(p):
    '''term : term MULTIPLY factor
            | term DIVIDE factor'''
    match [2]:
        case '*':
            p[0] = Expr(value=BinOp(left=p[1], op=Mult(), right=p[3]))
        case '/':
            p[0] = Expr(value=BinOp(left=p[1], op=Div(), right=p[3]))


def p_expression_calc(p):
    '''expression : expression PLUS term
                  | expression MINUS term'''
    match p[2]:
        case '+':
            p[0] = Expr(value=BinOp(left=p[1], op=Add(), right=p[3]))
        case '-':
            p[0] = Expr(value=BinOp(left=p[1], op=Sub(), right=p[3]))


def p_expression_term(p):
    'expression : term'
    p[0] = p[1]


def p_term_factor(p):
    '''term : factor'''
    p[0] = p[1]


def p_factor_expr(p):
    '''factor : LPAREN expression RPAREN
            | literal'''
    p[0] = p[2]


def p_error(p):
    pass


parser = yacc.yacc(debug=False)

text = ""
def dfs(graph):
    global text
    if isinstance(graph, Expr):
        for i in graph.child: dfs(i)
        text += str(graph.leaf) + ' '
    else: text += str(graph) + ' '

# compile
def compile(code):
    global error_p
    global text
    text = ""
    endcode = parser.parse(code)
    if error_p: return False
    dfs(endcode)
    endtext = ""
    for i in text.split():
        endtext = endtext + i + ' '
    return endtext

if __name__ == "__main__":
    s = ""
    while True:
        t = input('>>')
        if t == "run" or t == 'r': break
        s += t
    result = compile(s)
    print(result)