import celexer
tokens = celexer.tokens

from .ply import yacc

from ast import *

tokenlist = []
preclist = []

emit_code = 1


def p_literal(p):  # function call (returned value), number, string, list, etc
    '''literal : INTEGER
               | FLOAT
               | STRING
               | BOOLEAN
               | NONE
               | ID LPAREN args RPAREN'''


def p_args(p):
    '''args : '''


def p_positional_args(p):  # func(a, b)
    '''posargs : '''


def p_asterik_args(p):  # func(*a, **b)
    '''astargs : '''


def p_keyword_args(p):  # func(a=a, b=b)
    '''keyargs : '''


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


def p_term_calc(p):
    '''term : term MULTIPLY factor
            | term DIVIDE factor'''
    match [2]:
        case '*':
            p[0] = Expr(value=BinOp(left=p[1], op=Mult(), right=p[3]))
        case '/':
            p[0] = Expr(value=BinOp(left=p[1], op=Div(), right=p[3]))


def p_term_factor(p):
    'term : factor'
    p[0] = p[1]


def p_factor_expr(p):
    'factor : LPAREN expression RPAREN'
    p[0] = p[2]


def p_subtitute(p):
    '''subtitute: ID EQ literal'''


def p_error(p):
    pass


yacc = yacc.yacc(debug=False)
