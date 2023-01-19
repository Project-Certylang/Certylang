import celexer
tokens = celexer.tokens

from .ply import yacc

tokenlist = []
preclist = []

emit_code = 1


def p_error(p):
    pass


yacc = yacc.yacc(debug=False)
