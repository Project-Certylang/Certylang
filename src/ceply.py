import sys

import ceparser

if len(sys.argv) == 1:
    print("usage : ceply.py [-nocode] inputfile")
    raise SystemExit

if len(sys.argv) == 3:
    if sys.argv[1] == '-nocode':
        ceparser.emit_code = 0
    else:
        print("Unknown option '%s'" % sys.argv[1])
        raise SystemExit
    filename = sys.argv[2]
else:
    filename = sys.argv[1]

ceparser.yacc.parse(open(filename).read())

print("""
if __name__ == '__main__':
    from ply import *
    yacc.yacc()
""")