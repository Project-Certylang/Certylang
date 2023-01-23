from ply import lex


# expected input : type of keyword (also token name)
class KeywordManager:
    def __init__(self):
        self.keywords = {}
    
    def add_keywords(self, keywords: dict):
        for key, value in keywords.items():
            if key in self.keywords:
                raise ValueError(f"Keyword {key} already exists")
            self.keywords[key] = value
    
    def __iadd__(self, keywords: dict):
        self.add_keywords(keywords)
        return self

    def get_all(self):
        return tuple(self.keywords.values())

    def get(self, key, default=None):
        return self.keywords.get(key, default)

keywords = KeywordManager()


type_tokens = (  # for guessing literal types
    'INTEGER', # int
    'FLOAT', # float
    'STRING',  # str
    'BOOLEAN',  # bool
    #  'LIST',  Removed List - It should be done in parser level
    #  'TUPLE',  Removed Tuple - Same with list
    #  'DICTIONARY',  Removed Dictionary - Same with list
    #  'CALLABLE', Removed Callable - Same with lsit
)

keywords += {
    'int': 'ANNOINTEGER',
    'float': 'ANNOFLOAT',
    'str': 'ANNOSTRING',
    'bool': 'ANNOBOOLEAN',
    'list': 'ANNOLIST',
    'tuple': 'ANNOTUPLE',
    'dict': 'ANNODICTIONARY',
    'callable': 'ANNOCALLABLE',
    'none': 'NONE'
}


def optws_wrap(t, *, left=False, right=False, required=False):
    if required:
        optws = "(?:\s+)"
    else:
        optws = "(?:\s*)"
    r = t
    if left:
        r = optws + r
    if right:
        r = r + optws
    return r


t_INTEGER = optws_wrap(r"\d+", left=True)
t_FLOAT = optws_wrap(r"\d+\.\d+", left=True)
t_STRING = optws_wrap(r"'.*?'|\".*?\"", left=True)  # check docstring separately
t_BOOLEAN = optws_wrap(r"true|false", left=True)


keywords += {
    'if': 'IF',
    'for': 'FOR',
    'while': 'WHILE',
    'match': 'MATCH',
    'case': 'CASE'
}

keywords += {
    'var': 'VAR',  # variable
    'class': 'CLASS',  # class
    'function': 'FUNCTION',  # function
}

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
t_DEQ = optws_wrap(r"==", left=True, right=True)
t_EQ = optws_wrap(r"=", left=True, right=True)
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
    + special_tokens
    + comment_tokens
    + operation_tokens
    + keywords.get_all()
)

IDRule = r"[a-zA-Z_][a-zA-Z0-9_]*"

@lex.TOKEN(IDRule)
def t_ID(t):
    t.type = keywords.get(t.value, 'ID')
    return t

def t_WHITESPACE(t):
    r"\s+"
    pass

t_NEWLINE = r"\n"
t_DOT = r"\."


literals = []
t_ignore = '\t'


def t_error(t):
    print("%d: Illegal character '%s'" % (t.lexer.lineno, t.value[0]))
    print(t.value)
    t.lexer.skip(1)
    

t_PSARG = r'\*' + r'(' + IDRule + r')' + "?"
t_KWARG = r'\*\*' + IDRule
    

lexer = lex.lex()

# debug code
if __name__ == "__main__":
    lexer.input(input('>>'))
    while True:
        tok = lexer.token()
        if not tok: break
        print(":", tok)