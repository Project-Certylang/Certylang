from ply import lex

type_tokens = (  # for guessing literal types
    'NUMBER', # int, float
    'STRING',  # str
    'BOOLEAN',  # bool
    'LIST',  # list
    'TUPLE',  # tuple
    'DICTIONARY', # dict
    'CALLABLE', # callable
    'NONE',  # none
)

control_tokens = (
    'IF',  # if
    'FOR',  # for
    'WHILE',  # while
    'MATCH',  # match case
    'CASE', # match case
)

define_tokens = (
    'VAR',  # variable
    'CLASS',  # class
    'FUNCTION',  # function
)

special_tokens = (
    'LPAREN',  # left parentheses, (
    'RPAREN',  # right parentheses, )
    'LBRACE',  # left brace, [
    'RBRACE',  # right brace, ]
    'LBRACKET',  # left bracket, {
    'RBRACKET',  # riht bracket, }
    'GT',  # grater than, >
    'LT',  # less than, <
    'EQ',  # equal, =
    'DEQ',  # double equal, ==
    'NOT',  # not, !
)

comment_tokens = (  # js-like comment
    'COMMENT',  # single-line comment, //
    'MLCOMMENT',  # mutli-line comment, /**/
)

tokens = (
type_tokens
+ control_tokens
+ define_tokens
+ special_tokens
+ comment_tokens
)


literals = []
t_ignore = ' \t'


##### Comment
def t_COMMENT(t):
    r"//.*"
    pass

def t_MLCOMMENT(t):
    r"/\*(.|\n)*\*/"
    pass
##### Comment END


def t_error(t):
    print("%d: Illegal character '%s'" % (t.lexer.lineno, t.value[0]))
    print(t.value)
    t.lexer.skip(1)

lex.lex()

if __name__ == '__main__':
    lex.runmain()