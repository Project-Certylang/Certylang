from ply import lex

type_tokens = (  # for guessing literal types
    'INTEGER', # int
    'FLOAT', # float
    'STRING',  # str
    'BOOLEAN',  # bool
    #  'LIST',  Removed List - It should be done in parser level
    #  'TUPLE',  Removed Tuple - Same with list
    #  'DICTIONARY',  Removed Dictionary - Same with list
    #  'CALLABLE', Removed Callable - Same with lsit
    'NONE',  # none,
    'ANNOINTEGER', # 
    'ANNOFLOAT', #
    'ANNOSTRING', #
    'ANNOBOOLEAN', #,
    'ANNOLIST',
    'ANNOTUPLE',
    'ANNODICTIONARY',
    'ANNOCALLABLE',
    'ANNONONE'
)


def optws_wrap(t, *, left=False, right=False, required=False):
    if required:
        optws = "(?:\s+)"
    else:
        optws = "(?:\s*)"
    r = t
    if left:
        r = optws + t
    if right:
        r = t + optws
    return r


t_INTEGER = optws_wrap(r"\d+", left=True)
t_FLOAT = optws_wrap(r"\d+\.\d+", left=True)
t_STRING = optws_wrap(r"'.*?'|\".*?\"", left=True)  # check docstring separately
t_BOOLEAN = optws_wrap(r"true|false", left=True)
t_NONE = optws_wrap(r"none", left=True)
t_ANNOINTEGER = r"int"
t_ANNOFLOAT = r"float"
t_ANNOSTRING = r"str"
t_ANNOBOOLEAN = r"bool"
t_ANNOLIST = r"list"
t_ANNOTUPLE = r"tuple"
t_ANNODICTIONARY = r"dict"
t_ANNOCALLABLE = r"callable"
t_ANNONONE = r"none"

control_tokens = (
    'IF',  # if
    'FOR',  # for
    'WHILE',  # while
    'MATCH',  # match case
    'CASE', # match case
)

t_IF = optws_wrap(r"if", right=True, required=True)
t_FOR = optws_wrap(r"for", right=True, required=True)
t_WHILE = optws_wrap(r"while", right=True, required=True)
t_MATCH = optws_wrap(r"match", right=True, required=True)
t_CASE = optws_wrap(r"case", right=True, required=True)

define_tokens = (
    'VAR',  # variable
    'CLASS',  # class
    'FUNCTION',  # function
)

t_VAR = optws_wrap(r"var", right=True)
t_CLASS = optws_wrap(r"class", right=True, required=True)
t_FUNCTION = optws_wrap(r"function", right=True, required=True)

operation_tokens = (
    'PLUS',  # +
    'MINUS',  # -
    'DIVIDE',  # /
    'MULTIPLY',  # *
)

t_PLUS = optws_wrap(r"\+", left=True, right=True)
t_MINUS = optws_wrap(r"-", left=True, right=True)
t_DIVIDE = optws_wrap(r"/", left=True, right=True)
t_MULTIPLY = optws_wrap(r"\*", left=True, right=True)

special_tokens = (
    'LPAREN',  # left parentheses, (
    'RPAREN',  # right parentheses, )
    'LBRACE',  # left brace, [
    'RBRACE',  # right brace, ]
    'LBRACKET',  # left bracket, {
    'RBRACKET',  # riht bracket, }
    'GT',  # grater than, >
    'GE',  # greater than or equal to, >=
    'LT',  # less than, <
    'LE',  # less than or equal to, <=
    'EQ',  # equal, =
    'DEQ',  # double equal, ==
    'NOT',  # not, !
    'COMMA', # comma, ,
    'COLON', # colon, ;
)

t_LPAREN = optws_wrap(r"\(", right=True)
t_RPAREN = optws_wrap(r"\)", left=True)
t_LBRACE = optws_wrap(r"\[", right=True)
t_RBRACE = optws_wrap(r"\]", left=True)
t_LBRACKET = optws_wrap(r"\{", right=True)
t_RBRACKET = optws_wrap(r"\}", left=True)
t_GT = optws_wrap(r">", left=True, right=True)
t_GE = optws_wrap(r">=", left=True, right=True)
t_LT = optws_wrap(r"<", left=True, right=True)
t_LE = optws_wrap(r"<=", left=True, right=True)
t_EQ = optws_wrap(r"=", left=True, right=True)
t_DEQ = optws_wrap(r"==", left=True, right=True)
t_NOT = optws_wrap(r"!", left=True)
t_COMMA = optws_wrap(r",", left=True, right=True)
t_COLON = optws_wrap(r";", right=True)

comment_tokens = (  # js-like comment
    'COMMENT',  # single-line comment, //
    'MLCOMMENT',  # mutli-line comment, /**/
)

def t_COMMENT(t):
    r"//.*"
    pass

def t_MLCOMMENT(t):
    r"/\*(.|\n)*?\*/"
    pass

tokens = (
    (
        'ID',
        'WHITESPACE',
        'NEWLINE',
        'DOT',
        'PSARG',
        'KWARG'
    )
    + type_tokens
    + control_tokens
    + define_tokens
    + special_tokens
    + comment_tokens
    + operation_tokens
)

t_ID = r"[a-zA-Z_]+[a-zA-Z0-9_]*"

t_WHITESPACE = r"\s+"
t_NEWLINE = r"\n"
t_DOT = r"\."


literals = []
t_ignore = '\t'


def t_error(t):
    print("%d: Illegal character '%s'" % (t.lexer.lineno, t.value[0]))
    print(t.value)
    t.lexer.skip(1)
    

t_PSARG = r'\*' + t_ID + "?"
t_KWARG = r'\*\*' + t_ID
    

lexer = lex.lex()

# debug code
if __name__ == "__main__":
    lexer.input(input('>>'))
    while True:
        tok = lexer.token()
        if not tok: break
        print(":", tok)