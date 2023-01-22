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

t_INTEGER = r"\d+"
t_FLOAT = r"\d+.\d+"
t_STRING = r"'.*?'|\".*?\""  # check docstring separately
t_BOOLEAN = r"true|false"
t_NONE = r"none"
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

t_IF = r"if"
t_FOR = r"for"
t_WHILE = r"while"
t_MATCH = r"match"
t_CASE = r"case"

define_tokens = (
    'VAR',  # variable
    'CLASS',  # class
    'FUNCTION',  # function
)

t_VAR = r"var"
t_CLASS = r"class"
t_FUNCTION = r"function"

operation_tokens = (
    'PLUS',  # +
    'MINUS',  # -
    'DIVIDE',  # /
    'MULTIPLY',  # *
)

t_PLUS = r"\+"
t_MINUS = r"-"
t_DIVIDE = r"/"
t_MULTIPLY = r"\*"

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

t_LPAREN = r"\("
t_RPAREN = r"\)"
t_LBRACE = r"\["
t_RBRACE = r"\]"
t_LBRACKET = r"\{"
t_RBRACKET = r"\}"
t_GT = r">"
t_GE = r">="
t_LT = r"<"
t_LE = r"<="
t_EQ = r"="
t_DEQ = r"=="
t_NOT = r"!"
t_COMMA = r","
t_COLON = r";"

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
t_WHITESPACE = r"\s"
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