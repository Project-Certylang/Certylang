import celexer
tokens = celexer.tokens

from ply import yacc, lex

from ast import *

tokenlist = []
preclist = []

emit_code = 1

'''
Define Variable  - substitute
Change Variable Value  - substitute

Define Function  - def
Call Function  - call
'''


def p_program(p):
    '''program : command'''
    p[0] = p[1]


def p_command(p):
    '''command : substitute
               | def
               | call
               | NEWLINE
               | command NEWLINE command
               | command ';' command
               | command NEWLINE ';' command'''
    if len(p) == 2:
        if p[1] == '\n':
            return
        p[0] = [p[1]]
    else:
        p[0] = p[1].append(p[3])


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
               | id
               | expression'''
    p[0] = p[1]


def p_subsitute(p):
    '''substitute : VAR '<' annotation '>' WHITESPACE ID EQ literal
                  | VAR '<' annotation '>' ID
                  | ID EQ literal'''
    if len(p) == 8:
        p[0] = AnnAssign(target=Name(id=p[5].targets[0].id, ctx=Store()), annotation=p[3], value=p[7])
    elif len(p) == 6:
        p[0] = AnnAssign(target=Name(id=p[5].targets[0].id, ctx=Store()), annotation=p[3], value=None)
    elif len(p) == 4:
        p[0] = Assign(targets=[Name(id=p[1], ctx=Store())], value=p[3])


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


# function definition
def p_func_init(p):
    """def : FUNCTION ID '(' ')' '{' defbody '}'
           | FUNCTION ID '(' defargs ')' '{' defbody '}'"""
    if len(p) == 8:
        p[0] = FunctionDef(
            name=p[2],
            args=arguments(
                posonlyargs=[],
                args=[],
                kwonlyargs=[],
                kw_defaults=[],
                defaults=[]
            ),
            body=[
                p[6]
            ],
            decorator_list=[
                # TODO
            ]
        )
    else:
        p[0] = FunctionDef(
            name=p[2],
            args=p[4].make_args(),
            body=[
                p[6]
            ],
            decorator_list=[
                # TODO
            ]
        )


def p_def_body(p):
    '''defbody : command'''
    p[0] = p[1]


class FunctionArgument:
    def __init__(self, arg=None, annotation=None, default=None, psarg=False, vrarg=False, kwarg=False):
        self.default = default
        self.arg = arg
        self.annotation = annotation
        self.is_positional_sign = psarg  # /
        self.is_keyword_sign = kwarg  # **
        self.is_var_sign = vrarg  # *
    
    def make_arg(self):
        return arg(arg=self.arg, annotation=self.annotation)


class FunctionArgumentManager:
    def __init__(self, start_arg: FunctionArgument):
        self.pos_used = start_arg.is_positional_sign
        self.var_used = start_arg.is_var_sign
        self.kw_used = start_arg.is_keyword_sign
        
        self.force_default = start_arg.default is not None
        self.defaults = []
        self.kw_defaults = []
        
        self.vararg = None
        self.kwarg = None
        
        self.positional_args = []  # positional only
        self.normal_args = []  # positional, keyword
        self.keyword_args = []  # keyword only
        if self.var_used:
            self.vararg = start_arg.make_arg()
        elif self.kw_used:
            if start_arg:
                raise SyntaxError("positional argument follows keyword-only argument")
            self.kwarg = start_arg.make_arg()
        else:
            self.normal_args.append(start_arg)
        
    def put_arg(self, arg: FunctionArgument):
        if arg.is_positional_sign:
            if self.pos_used:
                raise SyntaxError("duplicate '/' in function definition")
            if self.var_used:
                raise SyntaxError("positional argument follows keyword-only argument")
            if self.kw_used:
                raise SyntaxError("argument cannot follows keyword argument")
            self.pos_used = True
            self.positional_args = self.normal_args.copy()
            self.normal_args = []
        elif arg.is_keyword_sign:
            if self.kw_used:
                raise SyntaxError("duplicate '**' in function definition")
            self.kw_used = True
            self.kwarg = arg.make_arg()
        elif arg.is_var_sign:
            if self.var_used:
                raise SyntaxError("duplicate '*' in function definition")
            if self.kw_used:
                raise SyntaxError("argument cannot follows keyword argument")
            self.var_used = True
            self.vararg = arg.make_arg()
        else:
            if arg.default is not None:
                self.force_default = True
                if self.var_used:
                    self.kw_defaults.append(arg.default)
                else:
                    self.defaults.append(arg.default)
            else:
                if self.force_default:
                    raise SyntaxError("non-default argument follows default argument")
                
            if self.kw_used:
                raise SyntaxError("argument cannot follows keyword argument")
            elif self.var_used:
                self.keyword_args.append(arg)
            else:
                self.normal_args.append(arg.make_arg())
                    
    
    def make_args(self):
        return arguments(
            posonlyargs=self.positional_args,
            args=self.normal_args,
            kwonlyargs=self.keyword_args,
            kw_defaults=self.kw_defaults,
            defaults=self.defaults,
            kwargs=self.kwarg,
            vararg=self.vararg
        )


def p_func_args(p):
    '''defargs : defargs COMMA defarg
               | defarg'''
    if len(p) == 2:
        p[0] = FunctionArgumentManager(p[1])
    else:
        p[1].put_arg(p[3])
        p[0] = p[1]


def p_func_arg(p):
    """defarg : ID '<' annotation '>'
              | ID '<' annotation '>' EQ literal
              | '/'
              | PSARG
              | KWARG"""
    if len(p) >= 4:
        o = FunctionArgument(arg=p[1], annotation=p[3])
        if len(p) == 6:
            o.default = p[5]
    else:  # '/', '*', '*asdf', '**asdf'
        if p[1] == '/':
            o = FunctionArgument(psarg=True)
        elif p[1] == '*':
            o = FunctionArgument(vrarg=True)
        elif p[1].startswith('**'):
            o = FunctionArgument(kwarg=True, arg=p[1][2:])
        elif p[1].startswith('*'):
            o = FunctionArgument(vrarg=True, arg=p[1][1:])
    p[0] = o
        

# function definition end

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
    '''term : factor
            | literal'''
    p[0] = p[1]


def p_factor_expr(p):
    '''factor : LPAREN expression RPAREN'''
    p[0] = p[2]


def p_error(p):
    pass

parser = yacc.yacc(debug=False, start="program")


if __name__ == "__main__":
    s = []
    while True:
        t = input('>>')
        if t == "run" or t == 'r': break
        s.append(t)
    print("--------------------")
    print("\n".join(s))
    print("--------------------")
    result = parser.parse("\n".join(s))
    print(dump(Module(body=result), indent=4))