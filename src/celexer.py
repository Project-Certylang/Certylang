from ply import lex

tokens = (
    'ID', 'QLITERAL', 'NUMBER',
)

literals = [';', ',', '<', '>', '|', ':']
t_ignore = ' \t'


t_ID = r'[a-zA-Z_][a-zA-Z_0-9]*'  # ?
t_QLITERAL  = r'''(?P<quote>['"]).*?(?P=quote)'''  # ?
t_NUMBER = r'\d+'


##### Comment
def t_ccomment(t):
    r'/\*(.|\n)*?\*/'
    t.lexer.lineno += t.value.count('\n')

t_ignore_cppcomment = r'//.*'
##### Comment END

def t_NEWLINE(t):
    r'\n'
    t.lexer.lineno += 1


def t_error(t):
    print("%d: Illegal character '%s'" % (t.lexer.lineno, t.value[0]))
    print(t.value)
    t.lexer.skip(1)

lex.lex()

if __name__ == '__main__':
    lex.runmain()