# PLY (Python Lex-Yacc)

# Ply (Python Lex-YACC)

This document provides an overview of lexing and parsing with PLY. Given

이 문서는 Ply와의 Lexing 및 Parsing에 대한 개요를 제공합니다. 주어진
the intrinsic complexity of parsing, I strongly advise that you read (or

구문 분석의 본질적인 복잡성, 나는 당신이 읽는 것을 강력히 권고합니다 (또는
at least skim) this entire document before jumping into a big

적어도 탈지)이 전체 문서가 큰 것으로 뛰어 들기 전에
development project with PLY.

Ply와 함께 개발 프로젝트.

The current version requires Python 3.6 or newer. If you\'re using an

현재 버전에는 Python 3.6 이상이 필요합니다. 당신이 an을 사용하는 경우
older version of Python, use one of the historical releases.

이전 버전의 Python은 역사적 릴리스 중 하나를 사용합니다.

## Introduction

## 소개

PLY is a pure-Python implementation of the compiler construction tools

Ply는 컴파일러 구성 도구의 순수한 파이썬 구현입니다.
lex and yacc. The main goal of PLY is to stay fairly faithful to the way

Lex와 YACC. Ply의 주요 목표는
in which traditional lex/yacc tools work. This includes supporting

전통적인 LEX/YACC 도구가 작동합니다. 여기에는 지원이 포함됩니다
LALR(1) parsing as well as providing extensive input validation, error

LALR (1) 구문 분석 및 광범위한 입력 검증, 오류 제공
reporting, and diagnostics. Thus, if you\'ve used yacc in another

보고 및 진단. 따라서, 당신이 다른 사람에게 yacc를 사용했다면
programming language, it should be relatively straightforward to use

프로그래밍 언어, 사용하는 것이 비교적 간단해야합니다.
PLY.

Early versions of PLY were developed to support an Introduction to

초기 버전의 Ply는 다음에 대한 소개를 지원하기 위해 개발되었습니다.
Compilers Course I taught in 2001 at the University of Chicago. Since

컴파일러 코스 시카고 대학교에서 2001 년에 가르쳤습니다. 부터
PLY was primarily developed as an instructional tool, you will find it

Ply는 주로 교육 도구로 개발되었습니다.
to be fairly picky about token and grammar rule specification. In part,

토큰과 문법 규칙 사양에 대해 상당히 까다 롭습니다. 일부,
this added formality is meant to catch common programming mistakes made

이 추가 형식은 일반적인 프로그래밍 실수를 포착하기위한 것입니다.
by novice users. However, advanced users will also find such features to

초보자 사용자. 그러나 고급 사용자는 이러한 기능도
be useful when building complicated grammars for real programming

실제 프로그래밍을 위해 복잡한 문법을 구축 할 때 유용하십시오
languages. It should also be noted that PLY does not provide much in the

언어. 또한 Ply는
way of bells and whistles (e.g., automatic construction of abstract

종소리와 휘파람의 방법 (예 : 초록의 자동 구성
syntax trees, tree traversal, etc.). Nor would I consider it to be a

구문 트리, 트리 트래버스 등). 나는 그것을 a라고 생각하지 않을 것입니다
parsing framework. Instead, you will find a bare-bones, yet fully

구문 분석 프레임 워크. 대신, 당신은 베어 본을 찾을 수 있지만 완전히
capable lex/yacc implementation written entirely in Python.

Python에 전적으로 작성된 유능한 LEX/YACC 구현.

The rest of this document assumes that you are somewhat familiar with

이 문서의 나머지 부분은 당신이 다소 익숙하다고 가정합니다.
parsing theory, syntax directed translation, and the use of compiler

구문 분석 이론, 구문 지시 된 번역 및 컴파일러 사용
construction tools such as lex and yacc in other programming languages.

다른 프로그래밍 언어의 Lex 및 YACC와 같은 건설 도구.
If you are unfamiliar with these topics, you will probably want to

이 주제에 익숙하지 않다면 아마도
consult an introductory text such as \"Compilers: Principles,

\ "컴파일러 : 원리, 예 : 소개 텍스트를 참조하십시오.
Techniques, and Tools\", by Aho, Sethi, and Ullman. O\'Reilly\'s \"Lex

Aho, Sethi 및 Ullman의 기술 및 도구 \ ". O \ 'Reilly \'s \"lex
and Yacc\" by John Levine may also be handy. In fact, the O\'Reilly book

그리고 John Levine의 Yacc \ "도 편리 할 수도 있습니다. 실제로 O \ 'Reilly Book
can be used as a reference for PLY as the concepts are virtually

개념이 사실상이므로 Ply에 대한 참조로 사용할 수 있습니다.
identical.

## PLY Overview

PLY consists of two separate modules; `lex.py` and `yacc.py`, both of

Ply는 두 개의 개별 모듈로 구성됩니다. `lex.py`와`yacc.py`
which are found in a Python package called `ply`. The `lex.py` module is

`ply`라는 파이썬 패키지에서 발견됩니다. `lex.py` 모듈은입니다
used to break input text into a collection of tokens specified by a

입력 텍스트를
collection of regular expression rules. `yacc.py` is used to recognize

정규 표현 규칙 수집. `yacc.py`는 인식하는 데 사용됩니다
language syntax that has been specified in the form of a context free

컨텍스트 무료 형태로 지정된 언어 구문
grammar.

The two tools are meant to work together. Specifically, `lex.py`

두 도구는 함께 작동하기위한 것입니다. 구체적으로,`lex.py`
provides an interface to produce tokens. `yacc.py` uses this retrieve

토큰을 생산하는 인터페이스를 제공합니다. `yacc.py`는이 검색을 사용합니다
tokens and invoke grammar rules. The output of `yacc.py` is often an

토큰 및 문법 규칙을 호출합니다. `yacc.py '의 출력은 종종 an입니다
Abstract Syntax Tree (AST). However, this is entirely up to the user. If

초록 구문 트리 (AST). 그러나 이것은 전적으로 사용자에게 달려 있습니다. 만약에
desired, `yacc.py` can also be used to implement simple one-pass

원하는`yacc.py`는 간단한 원-패스를 구현하는 데 사용될 수 있습니다.
compilers.

Like its Unix counterpart, `yacc.py` provides most of the features you

Unix 상대와 마찬가지로`yacc.py '는 대부분의 기능을 제공합니다.
expect including extensive error checking, grammar validation, support

광범위한 오류 검사, 문법 검증, 지원을 포함하여 기대합니다.
for empty productions, error tokens, and ambiguity resolution via

빈산, 오류 토큰 및 모호성 해상도를 통해
precedence rules. In fact, almost everything that is possible in

우선 순위 규칙. 사실, 가능한 거의 모든 것이 가능합니다
traditional yacc should be supported in PLY.

전통적인 YACC는 Ply로 지원되어야합니다.

The primary difference between `yacc.py` and Unix `yacc` is that

`yacc.py`와 unix` yacc`의 주요 차이점은
`yacc.py` doesn\'t involve a separate code-generation process. Instead,

`yacc.py`는 별도의 코드 생성 프로세스를 포함하지 않습니다. 대신에,
PLY relies on reflection (introspection) to build its lexers and

Ply
parsers. Unlike traditional lex/yacc which require a special input file

파서. 특수 입력 파일이 필요한 기존 LEX/YACC와 달리
that is converted into a separate source file, the specifications given

별도의 소스 파일, 주어진 사양으로 변환됩니다.
to PLY *are* valid Python programs. This means that there are no extra

ply *는 * 유효한 파이썬 프로그램입니다. 이것은 추가가 없다는 것을 의미합니다
source files nor is there a special compiler construction step (e.g.,

소스 파일도 특수 컴파일러 구성 단계도 없습니다 (예 :
running yacc to generate Python code for the compiler).

컴파일러 용 Python 코드를 생성하기 위해 YACC를 실행합니다).

## Lex

`lex.py` is used to tokenize an input string. For example, suppose

`lex.py`는 입력 문자열을 토큰 화하는 데 사용됩니다. 예를 들어, 가정하십시오
you\'re writing a programming language and a user supplied the following

당신은 프로그래밍 언어를 작성하고 사용자가 다음을 제공했습니다.
input string:

입력 문자열 :

    x = 3 + 42 * (s - t)

A tokenizer splits the string into individual tokens:

토큰 화기는 문자열을 개별 토큰으로 나눕니다.

    'x','=', '3', '+', '42', '*', '(', 's', '-', 't', ')'

Tokens are usually given names to indicate what they are. For example:

토큰은 일반적으로 이름이 부여되어 자신의 이름을 나타냅니다. 예를 들어:

    'ID','EQUALS','NUMBER','PLUS','NUMBER','TIMES',
    'LPAREN','ID','MINUS','ID','RPAREN'

More specifically, the input is broken into pairs of token types and

보다 구체적으로, 입력은 토큰 유형의 쌍으로 나뉩니다.
values. For example:

    ('ID','x'), ('EQUALS','='), ('NUMBER','3'), 
    ('PLUS','+'), ('NUMBER','42'), ('TIMES','*'),
    ('LPAREN','('), ('ID','s'), ('MINUS','-'),

( 'lparen', '('), ( 'id', 's'), ( 'minus', '-'),
    ('ID','t'), ('RPAREN',')')

( 'id', 't'), ( 'rparen', ')'))

The specification of tokens is done by writing a series of regular

토큰의 사양은 일련의 정규를 작성하여 수행됩니다.
expression rules. The next section shows how this is done using

표현 규칙. 다음 섹션에서는 이것이 어떻게 사용되는지 보여줍니다
`lex.py`.

### Lex Example

The following example shows how `lex.py` is used to write a simple

다음 예는`lex.py`가 단순한 글을 쓰는 데 사용되는 방법을 보여줍니다.
tokenizer:

    # ------------------------------------------------------------
    # calclex.py
    #
    # tokenizer for a simple expression evaluator for

간단한 표현식 평가자를위한 # 토 케이저
    # numbers and +,-,*,/

# 번호 및 +,-,*,/
    # ------------------------------------------------------------
    import ply.lex as lex

ply.lex를 lex로 가져옵니다

    # List of token names.   This is always required

# 토큰 이름 목록. 이것은 항상 필요합니다
    tokens = (
       'NUMBER',
       'PLUS',
       'MINUS',
       'TIMES',

'타임스',
       'DIVIDE',
       'LPAREN',
       'RPAREN',
    )

    # Regular expression rules for simple tokens

# 간단한 토큰에 대한 정규 표현 규칙
    t_PLUS    = r'\+'
    t_MINUS   = r'-'
    t_TIMES   = r'\*'

t_times = r '\*'
    t_DIVIDE  = r'/'
    t_LPAREN  = r'\('
    t_RPAREN  = r'\)'

    # A regular expression rule with some action code

# 일부 조치 코드가있는 정규 표현 규칙
    def t_NUMBER(t):
        r'\d+'
        t.value = int(t.value)    
        return t

    # Define a rule so we can track line numbers

# 라인 번호를 추적 할 수 있도록 규칙을 정의합니다.
    def t_newline(t):

def t_newline (t) :
        r'\n+'
        t.lexer.lineno += len(t.value)

    # A string containing ignored characters (spaces and tabs)

# 무시 된 문자 (공백 및 탭)가 포함 된 문자열
    t_ignore  = ' \t'

    # Error handling rule
    def t_error(t):
        print("Illegal character '%s'" % t.value[0])
        t.lexer.skip(1)

    # Build the lexer

# Lexer를 구축하십시오
    lexer = lex.lex()

To use the lexer, you first need to feed it some input text using its

Lexer를 사용하려면 먼저 ITS를 사용하여 입력 텍스트를 공급해야합니다.
`input()` method. After that, repeated calls to `token()` produce

`input ()`메소드. 그 후,`token ()`produce에 대한 반복 전화
tokens. The following code shows how this works:

토큰. 다음 코드는 이것이 어떻게 작동하는지를 보여줍니다.

    # Test it out
    data = '''
    3 + 4 * 10
      + -20 *2
    '''

    # Give the lexer some input

# Lexer에게 입력을 제공하십시오
    lexer.input(data)

    # Tokenize
    while True:

사실이지만 :
        tok = lexer.token()
        if not tok: 

토크가 아닌 경우 :
            break      # No more input

# 더 이상 입력하지 마십시오
        print(tok)

When executed, the example will produce the following output:

실행되면 예제는 다음 출력을 생성합니다.

    $ python example.py

$ python example.py
    LexToken(NUMBER,3,2,1)
    LexToken(PLUS,'+',2,3)
    LexToken(NUMBER,4,2,5)
    LexToken(TIMES,'*',2,7)
    LexToken(NUMBER,10,2,10)
    LexToken(PLUS,'+',3,14)
    LexToken(MINUS,'-',3,16)
    LexToken(NUMBER,20,3,18)
    LexToken(TIMES,'*',3,20)
    LexToken(NUMBER,2,3,21)

Lexers also support the iteration protocol. So, you can write the above

Lexers는 또한 반복 프로토콜을 지원합니다. 따라서 위의 글을 쓸 수 있습니다
loop as follows:

다음과 같이 루프 :

    for tok in lexer:
        print(tok)

The tokens returned by `lexer.token()` are instances of `LexToken`. This

`lexer.token ()`에 의해 반환 된 토큰은`lextoken '의 인스턴스입니다. 이것
object has attributes `type`, `value`, `lineno`, and `lexpos`. The

객체에는`type`,`value`,`lineno '및`lexpos'가 있습니다. 그만큼
following code shows an example of accessing these attributes:

다음 코드는 이러한 속성에 액세스하는 예를 보여줍니다.

    # Tokenize
    while True:

사실이지만 :
        tok = lexer.token()
        if not tok: 
            break      # No more input

# 더 이상 입력하지 마십시오
        print(tok.type, tok.value, tok.lineno, tok.lexpos)

The `type` and `value` attributes contain the type and value of the

`type` 및`value '속성에는
token itself. `lineno` and `lexpos` contain information about the

토큰 자체. `Lineno`와`lexpos '에는 정보에 대한 정보가 포함되어 있습니다
location of the token. `lexpos` is the index of the token relative to

토큰의 위치. `lexpos '는
the start of the input text.

입력 텍스트의 시작.

### The tokens list

### 토큰 목록

All lexers must provide a list `tokens` that defines all of the possible

모든 Lexers는 가능한 모든 것을 정의하는 목록을 제공해야합니다.
token names that can be produced by the lexer. This list is always

Lexer가 제작할 수있는 토큰 이름. 이 목록은 항상입니다
required and is used to perform a variety of validation checks. The

필수이며 다양한 검증 점검을 수행하는 데 사용됩니다. 그만큼
tokens list is also used by the `yacc.py` module to identify terminals.

토큰 목록은`yacc.py` 모듈에서도 터미널을 식별하는 데 사용됩니다.

In the example, the following code specified the token names:

예에서 다음 코드는 토큰 이름을 지정했습니다.

    tokens = (
       'NUMBER',
       'PLUS',
       'MINUS',
       'TIMES',

'타임스',
       'DIVIDE',
       'LPAREN',
       'RPAREN',
    )

### Specification of tokens

### 토큰 사양

Each token is specified by writing a regular expression rule compatible

각 토큰은 정규 표현 규칙을 작성하여 지정됩니다.
with Python\'s `re` module. Each of these rules are defined by making

Python \ 's` re` 모듈과 함께. 이러한 각 규칙은 제작에 의해 정의됩니다
declarations with a special prefix `t_` to indicate that it defines a

특별 접두사`t_`가있는 선언은
token. For simple tokens, the regular expression can be specified as

토큰. 간단한 토큰의 경우 정규 표현식은 다음과 같이 지정할 수 있습니다.
strings such as this (note: Python raw strings are used since they are

이와 같은 문자열 (참고 : Python Raw Strings가 사용하기 때문에 사용됩니다.
the most convenient way to write regular expression strings):

정규 표현 문자열을 작성하는 가장 편리한 방법) :

    t_PLUS = r'\+'

In this case, the name following the `t_` must exactly match one of the

이 경우`t_`를 따르는 이름은 다음 중 하나와 정확히 일치해야합니다.
names supplied in `tokens`. If some kind of action needs to be

`Tokens`에 제공된 이름. 어떤 종류의 행동이 필요하다면
performed, a token rule can be specified as a function. For example,

수행 된 토큰 규칙은 함수로 지정할 수 있습니다. 예를 들어,
this rule matches numbers and converts the string into a Python integer:

이 규칙은 숫자와 일치하고 문자열을 파이썬 정수로 변환합니다.

    def t_NUMBER(t):
        r'\d+'
        t.value = int(t.value)
        return t

When a function is used, the regular expression rule is specified in the

함수가 사용되면 정규 표현 규칙이
function documentation string. The function always takes a single

함수 문자 문자열. 함수는 항상 단일이 필요합니다
argument which is an instance of `LexToken`. This object has attributes

`lextoken`의 인스턴스 인 인수. 이 개체에는 속성이 있습니다
of `type` which is the token type (as a string), `value` which is the

토큰 유형 (문자열로) 인`type`,`value '는
lexeme (the actual text matched), `lineno` which is the current line

Lexeme (실제 텍스트 일치),`Lineno '는 현재 줄입니다.
number, and `lexpos` which is the position of the token relative to the

숫자, 그리고`lexpos '는
beginning of the input text. By default, `type` is set to the name

입력 텍스트의 시작. 기본적으로`type`은 이름으로 설정됩니다.
following the `t_` prefix. The action function can modify the contents

`t_` 접두사 다음. 동작 함수는 내용을 수정할 수 있습니다
of the `LexToken` object as appropriate. However, when it is done, the

적절한 'lextoken'대상의. 그러나 완료되면
resulting token should be returned. If no value is returned by the

결과 토큰을 반환해야합니다. 값이없는 경우
action function, the token is discarded and the next token read.

액션 함수, 토큰이 폐기되고 다음 토큰이 읽습니다.

Internally, `lex.py` uses the `re` module to do its pattern matching.

내부적으로`lex.py`는`re` 모듈을 사용하여 패턴 일치를 수행합니다.
Patterns are compiled using the `re.VERBOSE` flag which can be used to

패턴은 사용될 수있는`re.verbose` 플래그를 사용하여 컴파일됩니다.
help readability. However, be aware that unescaped whitespace is ignored

가독성에 도움이됩니다. 그러나 에스카로운 공백은 무시된다는 점에 유의하십시오
and comments are allowed in this mode. If your pattern involves

이 모드에서 의견이 허용됩니다. 당신의 패턴이 포함된다면
whitespace, make sure you use `\s`. If you need to match the `#`

공백,`\ s`를 사용해야합니다. `#`와 일치 해야하는 경우
character, use `[#]`.

문자,`[#]`을 사용하십시오.

When building the master regular expression, rules are added in the

마스터 정규 표현식을 구축 할 때 규칙이 추가됩니다.
following order:

다음 순서 :

1.  All tokens defined by functions are added in the same order as they

1. 함수로 정의 된 모든 토큰은
    appear in the lexer file.

Lexer 파일에 나타납니다.
2.  Tokens defined by strings are added next by sorting them in order of

2. 문자열로 정의 된 토큰은 다음에 정렬하여 다음에 추가됩니다.
    decreasing regular expression length (longer expressions are added

정규 발현 길이 감소 (더 긴 표현이 추가됩니다
    first).

첫 번째).

Without this ordering, it can be difficult to correctly match certain

이 순서가 없으면 특정 일치하는 것이 어려울 수 있습니다.
types of tokens. For example, if you wanted to have separate tokens for

토큰의 종류. 예를 들어, 별도의 토큰을 원한다면
\"=\" and \"==\", you need to make sure that \"==\" is checked first. By

\ "= \"및 \ "== \", \ "== \"가 먼저 점검되어 있는지 확인해야합니다. 에 의해
sorting regular expressions in order of decreasing length, this problem

길이 감소 순서대로 정규 표현식 정렬,이 문제
is solved for rules defined as strings. For functions, the order can be

문자열로 정의 된 규칙에 대해 해결됩니다. 함수의 경우 순서가 될 수 있습니다
explicitly controlled since rules appearing first are checked first.

먼저 나타나는 규칙이 먼저 확인되므로 명시 적으로 제어됩니다.

To handle reserved words, you should write a single rule to match an

예약 된 단어를 처리하려면 일치하는 단일 규칙을 작성해야합니다.
identifier and do a special name lookup in a function like this:

다음과 같은 기능에서 식별자 및 특별 이름 조회를 수행하십시오.

    reserved = {
       'if' : 'IF',
       'then' : 'THEN',

'그런 다음': '그런 다음',
       'else' : 'ELSE',
       'while' : 'WHILE',

'while': 'while',
       ...
    }

    tokens = ['LPAREN','RPAREN',...,'ID'] + list(reserved.values())

    def t_ID(t):

def t_id (t) :
        r'[a-zA-Z_][a-zA-Z_0-9]*'
        t.type = reserved.get(t.value,'ID')    # Check for reserved words

t.type = reserved.get (t.value, 'id') # 예약 단어 확인
        return t

This approach greatly reduces the number of regular expression rules and

이 접근법은 정규 표현 규칙의 수를 크게 줄이고
is likely to make things a little faster.

일을 조금 더 빨리 만들 가능성이 높습니다.

Note: You should avoid writing individual rules for reserved words. For

참고 : 예약 된 단어에 대한 개별 규칙을 작성하지 않아야합니다. 을 위한
example, if you write rules like this:

예를 들어, 다음과 같은 규칙을 작성하는 경우 :

    t_FOR   = r'for'
    t_PRINT = r'print'

those rules will be triggered for identifiers that include those words

이러한 규칙은 해당 단어를 포함하는 식별자에 대해 트리거됩니다.
as a prefix such as \"forget\" or \"printed\". This is probably not what

\ "forget \"또는 \ "printed \"와 같은 접두사로. 이것은 아마도 무엇이 아닐 것입니다
you want.

### Token values

When tokens are returned by lex, they have a value that is stored in the

Lex가 토큰을 반환하면
`value` attribute. Normally, the value is the text that was matched.

`value` 속성. 일반적으로 값은 일치하는 텍스트입니다.
However, the value can be assigned to any Python object. For instance,

그러나 값은 모든 Python 객체에 할당 될 수 있습니다. 예를 들어,
when lexing identifiers, you may want to return both the identifier name

Lexing 식별자 일 때 식별자 이름을 모두 반환 할 수 있습니다.
and information from some sort of symbol table. To do this, you might

그리고 일종의 심볼 테이블의 정보. 이렇게 할 수 있습니다
write a rule like this:

다음과 같은 규칙을 작성하십시오.

    def t_ID(t):

def t_id (t) :
        ...
        # Look up symbol table information and return a tuple

# 기호 테이블 정보를 찾고 튜플을 반환합니다.
        t.value = (t.value, symbol_lookup(t.value))
        ...
        return t

It is important to note that storing data in other attribute names is

다른 속성 이름으로 데이터를 저장하는 것이 중요합니다.
*not* recommended. The `yacc.py` module only exposes the contents of the

* 권장되지 않습니다. `yacc.py '모듈은
`value` attribute. Thus, accessing other attributes may be unnecessarily

`value` 속성. 따라서 다른 속성에 액세스하는 것은 불필요하게 일 수 있습니다
awkward. If you need to store multiple values on a token, assign a

어색한. 토큰에 여러 값을 저장 해야하는 경우
tuple, dictionary, or instance to `value`.

튜플, 사전 또는 'value'로 인스턴스.

### Discarded tokens

To discard a token, such as a comment, define a token rule that returns

주석과 같은 토큰을 폐기하려면 반환하는 토큰 규칙을 정의합니다.
no value. For example:

    def t_COMMENT(t):
        r'\#.*'
        pass
        # No return value. Token discarded

Alternatively, you can include the prefix `ignore_` in the token

또는 토큰에 Prefix` ingore_`를 포함시킬 수 있습니다.
declaration to force a token to be ignored. For example:

토큰을 무시하도록 선언합니다. 예를 들어:

    t_ignore_COMMENT = r'\#.*'

Be advised that if you are ignoring many different kinds of text, you

여러 종류의 텍스트를 무시하고 있다면
may still want to use functions since these provide more precise control

더 정확한 제어를 제공하기 때문에 기능을 사용하고 싶을 수도 있습니다.
over the order in which regular expressions are matched (i.e., functions

정규 표현이 일치하는 순서 (즉, 함수
are matched in order of specification whereas strings are sorted by

문자열은 다음과 같이 정렬되는 반면 사양 순서대로 일치합니다.
regular expression length).

정규 표현 길이).

### Line numbers and positional information

### 줄 번호 및 위치 정보

By default, `lex.py` knows nothing about line numbers. This is because

기본적으로`lex.py`는 라인 번호에 대해 아무것도 모릅니다. 이 때문입니다
`lex.py` doesn\'t know anything about what constitutes a \"line\" of

`lex.py`는 \ "line \"을 구성하는 것에 대해 아무것도 알지 못합니다.
input (e.g., the newline character or even if the input is textual

입력 (예 : Newline 문자 또는 입력이 텍스트 인 경우
data). To update this information, you need to write a special rule. In

데이터). 이 정보를 업데이트하려면 특별 규칙을 작성해야합니다. ~ 안에
the example, the `t_newline()` rule shows how to do this:

예,`t_newline ()`규칙은 다음 방법을 보여줍니다.

    # Define a rule so we can track line numbers

# 라인 번호를 추적 할 수 있도록 규칙을 정의합니다.
    def t_newline(t):

def t_newline (t) :        r'\n+'
        t.lexer.lineno += len(t.value)

Within the rule, the `lineno` attribute of the underlying lexer

규칙 내에서, 기본 Lexer의`Lineno '속성
`t.lexer` is updated. After the line number is updated, the token is

`t.lexer`가 업데이트되었습니다. 줄 번호가 업데이트 된 후 토큰은
discarded since nothing is returned.

아무것도 반환되지 않기 때문에 폐기됩니다.

`lex.py` does not perform any kind of automatic column tracking.

`lex.py`는 어떤 종류의 자동 열 추적을 수행하지 않습니다.
However, it does record positional information related to each token in

그러나 각 토큰과 관련된 위치 정보를 기록합니다.
the `lexpos` attribute. Using this, it is usually possible to compute

`lexpos '속성. 이것을 사용하면 일반적으로 계산할 수 있습니다
column information as a separate step. For instance, just count

열 정보는 별도의 단계입니다. 예를 들어, 계산하십시오
backwards until you reach a newline:

Newline에 도달 할 때까지 거꾸로 :

    # Compute column.
    #     input is the input text string

# 입력은 입력 텍스트 문자열입니다
    #     token is a token instance
    def find_column(input, token):

def find_column (입력, 토큰) :
        line_start = input.rfind('\n', 0, token.lexpos) + 1
        return (token.lexpos - line_start) + 1

Since column information is often only useful in the context of error

열 정보는 종종 오류의 맥락에서만 유용하기 때문에
handling, calculating the column position can be performed when needed

핸들링, 열 위치 계산 필요할 때 수행 할 수 있습니다.
as opposed to doing it for each token. Note: If you\'re parsing a

각 토큰마다 수행하는 것과는 반대로. 참고 : 당신이 parsing a
language where whitespace matters (i.e., Python), it\'s probably better

공백이 중요한 언어 (즉, 파이썬), 아마도 더 나을 것입니다.
match whitespace as a token instead of ignoring it.

공백을 무시하는 대신 토큰으로 일치시킵니다.

### Ignored characters

### 문자를 무시했습니다

The special `t_ignore` rule is reserved by `lex.py` for characters that

특별`t_ignore` 규칙은`lex.py`가 캐릭터를 위해 예약합니다.
should be completely ignored in the input stream. Usually this is used

입력 스트림에서 완전히 무시해야합니다. 일반적으로 이것은 사용됩니다
to skip over whitespace and other non-essential characters. Although it

공백 및 기타 비 필수 캐릭터를 건너 뛸 수 있습니다. 비록
is possible to define a regular expression rule for whitespace in a

whitespace에 대한 정규 표현 규칙을 정의 할 수 있습니다.
manner similar to `t_newline()`, the use of `t_ignore` provides

`t_newline ()`과 유사한 방식으로`t_ignore`의 사용은 제공됩니다.
substantially better lexing performance because it is handled as a

실질적으로 더 나은 Lexing 성능은
special case and is checked in a much more efficient manner than the

특별한 경우 및 훨씬 더 효율적인 방식으로 확인됩니다.
normal regular expression rules.

The characters given in `t_ignore` are not ignored when such characters

`t_ignore`에 주어진 문자는 그러한 캐릭터 일 때 무시되지 않습니다.
are part of other regular expression patterns. For example, if you had a

다른 정규 표현 패턴의 일부입니다. 예를 들어, 당신이 a
rule to capture quoted text, that pattern can include the ignored

인용 된 텍스트를 캡처하는 규칙, 그 패턴은 무시 된 것을 포함 할 수 있습니다.
characters (which will be captured in the normal way). The main purpose

문자 (일반적인 방식으로 캡처 될 것입니다). 주된 목적
of `t_ignore` is to ignore whitespace and other padding between the

`t_ignore`의``t_ignore '는
tokens that you actually want to parse.

실제로 구문 분석하고 싶은 토큰.

### Literal characters

### 문자 문자

Literal characters can be specified by defining a variable `literals` in

리터럴 문자는 변수`wentals '를 정의하여 지정할 수 있습니다.
your lexing module. For example:

    literals = [ '+','-','*','/' ]

or alternatively:

또는 대안으로 :

    literals = "+-*/"

A literal character is a single character that is returned \"as is\"

문자 문자는 \ "Is \"로 반환되는 단일 문자입니다.
when encountered by the lexer. Literals are checked after all of the

렉서가 만났을 때. 리터럴은 모든 후에 확인됩니다
defined regular expression rules. Thus, if a rule starts with one of the

정의 정규 표현 규칙. 따라서 규칙이
literal characters, it will always take precedence.

문자 그대로의 캐릭터는 항상 우선합니다.

When a literal token is returned, both its `type` and `value` attributes

문자 그대로의 토큰이 반환되면`type`과`값 '속성이 모두
are set to the character itself. For example, `'+'`.

캐릭터 자체로 설정됩니다. 예를 들어,` '+'`.

It\'s possible to write token functions that perform additional actions

추가 작업을 수행하는 토큰 기능을 작성하는 것은 가능합니다.
when literals are matched. However, you\'ll need to set the token type

리터럴이 일치 할 때. 그러나 토큰 유형을 설정해야합니다.
appropriately. For example:

적절하게. 예를 들어:

    literals = [ '{', '}' ]

    def t_lbrace(t):
        r'\{'
        t.type = '{'      # Set token type to the expected literal

t.type = '{' # 세트 토큰 유형이 예상되는 리터럴에
        return t

        return t

    def t_rbrace(t):
        r'\}'
        t.type = '}'      # Set token type to the expected literal

t.type = '}' # 예상되는 리터럴에 토큰 유형을 설정
        return t

반환 t

### Error handling

The `t_error()` function is used to handle lexing errors that occur when

`t_error ()`함수는
illegal characters are detected. In this case, the `t.value` attribute

불법 문자가 감지됩니다. 이 경우`t.value` 속성입니다
contains the rest of the input string that has not been tokenized. In

토큰 화되지 않은 나머지 입력 문자열이 포함되어 있습니다. ~ 안에
the example, the error function was defined as follows:

예, 오류 함수는 다음과 같이 정의되었습니다.

    # Error handling rule
    def t_error(t):
        print("Illegal character '%s'" % t.value[0])
        t.lexer.skip(1)

In this case, we print the offending character and skip ahead one

이 경우, 우리는 불쾌한 캐릭터를 인쇄하고 앞서 건너 뜁니다.
character by calling `t.lexer.skip(1)`.

`t.lexer.skip (1)`을 호출하여 문자.

### EOF Handling

The `t_eof()` function is used to handle an end-of-file (EOF) condition

`t_eof ()`함수는 파일 끝 (EOF) 조건을 처리하는 데 사용됩니다.
in the input. As input, it receives a token type `'eof'` with the

입력에서. 입력대로, 그것은 토큰 유형` 'eof'`를
`lineno` and `lexpos` attributes set appropriately. The main use of this

`lineno`와`lexpos '속성은 적절하게 설정됩니다. 이것의 주요 용도
function is provide more input to the lexer so that it can continue to

함수는 Lexer에 더 많은 입력을 제공하여 계속 할 수 있습니다.
parse. Here is an example of how this works:

구문 분석. 다음은 이것이 어떻게 작동하는지에 대한 예입니다.

    # EOF handling rule
    def t_eof(t):

def t_eof (t) :
        # Get more input (Example)
        more = input('... ')

more = 입력 ( '...')        if more:

더 많은 경우 :
            t.lexer.input(more)
            return t.lexer.token()
        return None

The EOF function should return the next available token (by calling

EOF 함수는 다음에 사용 가능한 토큰을 반환해야합니다 (
`t.lexer.token())` or `None` to indicate no more data. Be aware that

`t.lexer.token ())`또는`none '은 더 이상 데이터를 표시하지 않습니다. 알고 있어야합니다
setting more input with the `t.lexer.input()` method does NOT reset

`t.lexer.input ()`메소드가 재설정되지 않음으로 더 많은 입력 설정
the lexer state or the `lineno` attribute used for position tracking.

Lexer 상태 또는 위치 추적에 사용되는 'Lineno'속성.
The `lexpos` attribute is reset so be aware of that if you\'re using it

`lexpos '속성은 재설정됩니다.
in error reporting.

### Building and using the lexer

### Lexer 건물 및 사용

To build the lexer, the function `lex.lex()` is used. For example:

Lexer를 구축하려면`lex.lex ()`함수가 사용됩니다. 예를 들어:

    lexer = lex.lex()

This function uses Python reflection (or introspection) to read the

이 기능은 Python Reflection (또는 내성)을 사용하여
regular expression rules out of the calling context and build the lexer.

정규 표현식은 호출 컨텍스트에서 제외하고 Lexer를 구축합니다.
Once the lexer has been built, two methods can be used to control the

Lexer가 구축되면 두 가지 방법을 사용하여 제어 할 수 있습니다.
lexer:

`lexer.input(data)`. Reset the lexer and store a new input string.

`lexer.input (data)`. Lexer를 재설정하고 새 입력 문자열을 저장하십시오.

`lexer.token()`. Return the next token. Returns a special `LexToken`

`lexer.token ()`. 다음 토큰을 반환하십시오. 특별한 'lextoken'을 반환합니다
instance on success or None if the end of the input text has been

입력 텍스트의 끝이있는 경우 성공 또는 없음 인스턴스
reached.

도달했다.

### The \@TOKEN decorator

### \ @token 데코레이터

In some applications, you may want to define tokens as a series of more

일부 응용 프로그램에서는 토큰을 일련의 더 많은 것으로 정의 할 수 있습니다.
complex regular expression rules. For example:

    digit            = r'([0-9])'
    nondigit         = r'([_A-Za-z])'
    identifier       = r'(' + nondigit + r'(' + digit + r'|' + nondigit + r')*)'        

    def t_ID(t):

def t_id (t) :
        # want docstring to be identifier above. ?????

# DocString이 위의 식별자가되기를 원합니다. ?????
        ...

In this case, we want the regular expression rule for `ID` to be one of

이 경우, 우리는`id`가 중 하나가되기를 원합니다.
the variables above. However, there is no way to directly specify this

위의 변수. 그러나이를 직접 지정할 방법이 없습니다.
using a normal documentation string. To solve this problem, you can use

일반 문서 문자열 사용. 이 문제를 해결하기 위해 사용할 수 있습니다
the `@TOKEN` decorator. For example:

`@token` 데코레이터. 예를 들어:

    from ply.lex import TOKEN

ply.lex import 토큰에서

    @TOKEN(identifier)
    def t_ID(t):

def t_id (t) :
        ...

This will attach `identifier` to the docstring for `t_ID()` allowing

이것은`t_id ()`reence에 대한 docstring에`identifier '를 첨부합니다.
`lex.py` to work normally. Naturally, you could use `@TOKEN` on all

`lex.py`는 정상적으로 일합니다. 당연히, 당신은 모두에`@token`을 사용할 수 있습니다.
functions as an alternative to using docstrings.

docstrings를 사용하는 대안으로 기능합니다.

### Debugging

For the purpose of debugging, you can run `lex()` in a debugging mode as

디버깅을 위해 디버깅 모드에서`lex ()`를 실행할 수 있습니다.
follows:

다음 :

    lexer = lex.lex(debug=True)

This will produce various sorts of debugging information including all

이것은 모두를 포함하여 다양한 종류의 디버깅 정보를 생성합니다.
of the added rules, the master regular expressions used by the lexer,

추가 규칙 중 Lexer가 사용한 마스터 정규 표현식
and tokens generating during lexing.

렉싱 중에 생성되는 토큰.

In addition, `lex.py` comes with a simple main function which will

또한`lex.py`는 간단한 주요 기능이 제공됩니다.
either tokenize input read from standard input or from a file specified

표준 입력 또는 지정된 파일에서 입력 토큰 화
on the command line. To use it, put this in your lexer:

명령 줄에서. 그것을 사용하려면 이것을 Lexer에 넣으십시오.

    if __name__ == '__main__':

__name__ == '__main__':
         lex.runmain()

Please refer to the \"Debugging\" section near the end for some more

끝 근처의 \ "디버깅 \"섹션을 참조하십시오.
advanced details of debugging.

디버깅의 고급 세부 사항.

### Alternative specification of lexers

### Lexers의 대체 사양

As shown in the example, lexers are specified all within one Python

예에서 볼 수 있듯이 Lexers는 하나의 파이썬 내에 모두 지정됩니다.
module. If you want to put token rules in a different module from the

기준 치수. 토큰 규칙을 다른 모듈에 넣으려면
one in which you invoke `lex()`, use the `module` keyword argument.

`lex ()`를 호출하는 것은 '모듈'키워드 인수를 사용하십시오.

For example, you might have a dedicated module that just contains the

예를 들어
token rules:

    # module: tokrules.py
    # This module just contains the lexing rules

#이 모듈에는 Lexing 규칙 만 포함됩니다

    # List of token names.   This is always required

# 토큰 이름 목록. 이것은 항상 필요합니다
    tokens = (
       'NUMBER',
       'PLUS',
       'MINUS',
       'TIMES',

'타임스',
       'DIVIDE',
       'LPAREN',
       'RPAREN',
    )

    # Regular expression rules for simple tokens

# 간단한 토큰에 대한 정규 표현 규칙
    t_PLUS    = r'\+'
    t_MINUS   = r'-'
    t_TIMES   = r'\*'

t_times = r '\*'
    t_DIVIDE  = r'/'
    t_LPAREN  = r'\('
    t_RPAREN  = r'\)'

    # A regular expression rule with some action code

# 일부 조치 코드가있는 정규 표현 규칙
    def t_NUMBER(t):
        r'\d+'
        t.value = int(t.value)    
        return t

    # Define a rule so we can track line numbers

# 라인 번호를 추적 할 수 있도록 규칙을 정의합니다.
    def t_newline(t):

def t_newline (t) :        r'\n+'
        t.lexer.lineno += len(t.value)

    # A string containing ignored characters (spaces and tabs)

# 무시 된 문자 (공백 및 탭)가 포함 된 문자열
    t_ignore  = ' \t'

    # Error handling rule
    def t_error(t):
        print("Illegal character '%s'" % t.value[0])
        t.lexer.skip(1)

Now, if you wanted to build a tokenizer from these rules from within a

이제이 규칙에서 토큰 화기를 구축하고 싶다면
different module, you would do the following (shown for Python

다른 모듈, 당신은 다음을 수행 할 것입니다 (Python에 표시됩니다.
interactive mode):

대화식 모드) :

    >>> import tokrules
    >>> lexer = lex.lex(module=tokrules)
    >>> lexer.input("3 + 4")
    >>> lexer.token()
    LexToken(NUMBER,3,1,1,0)
    >>> lexer.token()
    LexToken(PLUS,'+',1,2)
    >>> lexer.token()
    LexToken(NUMBER,4,1,4)
    >>> lexer.token()
    None
    >>>

The `module` option can also be used to define lexers from instances of

'모듈'옵션은 또한 인스턴스에서 Lexers를 정의하는 데 사용될 수도 있습니다.
a class. For example:

수업. 예를 들어:

    import ply.lex as lex

    class MyLexer(object):
        # List of token names.   This is always required

# 토큰 이름 목록. 이것은 항상 필요합니다
        tokens = (
           'NUMBER',
           'PLUS',
           'MINUS',
           'TIMES',

'타임스',
           'DIVIDE',
           'LPAREN',
           'RPAREN',
        )

        # Regular expression rules for simple tokens

# 간단한 토큰에 대한 정규 표현 규칙
        t_PLUS    = r'\+'
        t_MINUS   = r'-'
        t_TIMES   = r'\*'

t_times = r '\*'
        t_DIVIDE  = r'/'
        t_LPAREN  = r'\('
        t_RPAREN  = r'\)'

        # A regular expression rule with some action code

# 일부 조치 코드가있는 정규 표현 규칙
        # Note addition of self parameter since we're in a class

# 우리가 수업에 있기 때문에 자체 매개 변수 추가 참고
        def t_NUMBER(self,t):
            r'\d+'
            t.value = int(t.value)    
            return t

            return t

        # Define a rule so we can track line numbers

# 라인 번호를 추적 할 수 있도록 규칙을 정의합니다.
        def t_newline(self,t):
            r'\n+'
            t.lexer.lineno += len(t.value)

        # A string containing ignored characters (spaces and tabs)

# 무시 된 문자 (공백 및 탭)가 포함 된 문자열
        t_ignore  = ' \t'

        # Error handling rule
        def t_error(self,t):
            print("Illegal character '%s'" % t.value[0])
            t.lexer.skip(1)

        # Build the lexer

# Lexer를 구축하십시오
        def build(self,**kwargs):
            self.lexer = lex.lex(module=self, **kwargs)

        # Test it output
        def test(self,data):
            self.lexer.input(data)
            while True:

사실이지만 :
                 tok = self.lexer.token()
                 if not tok: 

토크가 아닌 경우 :
                     break
                 print(tok)

    # Build the lexer and try it out

# Lexer를 만들고 시도해보십시오
    m = MyLexer()
    m.build()           # Build the lexer

M.Build () # Lexer 빌드
    m.test("3 + 4")     # Test it

When building a lexer from class, *you should construct the lexer from

수업에서 Lexer를 구축 할 때 *Lexer를 건설해야합니다.
an instance of the class*, not the class object itself. This is because

클래스 객체 자체가 아닌 클래스*의 인스턴스*. 이 때문입니다
PLY only works properly if the lexer actions are defined by

Ply는 Lexer 조치가
bound-methods.

바운드 방법.

When using the `module` option to `lex()`, PLY collects symbols from the

`lex ()`에`module` 옵션을 사용하는 경우 Ply는 기호를 수집합니다.
underlying object using the `dir()` function. There is no direct access

`dir ()`함수를 사용하는 기본 객체. 직접 액세스가 없습니다
to the `__dict__` attribute of the object supplied as a module value.

모듈 값으로 제공되는 객체의`__dict__` 속성에.

Finally, if you want to keep things nicely encapsulated, but don\'t want

마지막으로, 당신이 물건을 멋지게 캡슐화하고 싶다면
to use a full-fledged class definition, lexers can be defined using

본격적인 클래스 정의를 사용하려면 Lexers를 사용하여 정의 할 수 있습니다.
closures. For example:

    import ply.lex as lex

    import ply.lex as lex

    # List of token names.   This is always required

# 토큰 이름 목록. 이것은 항상 필요합니다
    tokens = (
      'NUMBER',
      'PLUS',
      'MINUS',
      'TIMES',

'타임스',      'DIVIDE',
      'LPAREN',
      'RPAREN',
    )

    def MyLexer():
        # Regular expression rules for simple tokens
        t_PLUS    = r'\+'
        t_MINUS   = r'-'
        t_TIMES   = r'\*'

t_times = r '\*'
        t_DIVIDE  = r'/'
        t_LPAREN  = r'\('
        t_RPAREN  = r'\)'

        # A regular expression rule with some action code

# 일부 조치 코드가있는 정규 표현 규칙
        def t_NUMBER(t):
            r'\d+'
            t.value = int(t.value)    
            return t

        # Define a rule so we can track line numbers

# 라인 번호를 추적 할 수 있도록 규칙을 정의합니다.
        def t_newline(t):

        def t_newline(t):
            r'\n+'
            t.lexer.lineno += len(t.value)

        # A string containing ignored characters (spaces and tabs)

# 무시 된 문자 (공백 및 탭)가 포함 된 문자열
        t_ignore  = ' \t'

        # Error handling rule
        def t_error(t):
            print("Illegal character '%s'" % t.value[0])
            t.lexer.skip(1)

        # Build the lexer from my environment and return it    

# 내 환경에서 Lexer를 구축하고 반환하십시오.
        return lex.lex()

Important note: If you are defining a lexer using a class or closure, be

중요한 참고 사항 : 클래스 또는 폐쇄를 사용하여 Lexer를 정의하는 경우
aware that PLY still requires you to only define a single lexer per

Ply는 여전히 당신이 여전히 단일 Lexer 만 정의해야한다는 것을 알고 있습니다.
module (source file). There are extensive validation/error checking

모듈 (소스 파일). 광범위한 검증/오류 확인이 있습니다
parts of the PLY that may falsely report error messages if you don\'t

당신이 오류 메시지를 잘못보고 할 수있는 플라이의 일부는 당신이하지 않으면
follow this rule.

이 규칙을 따르십시오.

### Maintaining state

### 상태 유지

In your lexer, you may want to maintain a variety of state information.

Lexer에서는 다양한 상태 정보를 유지할 수 있습니다.
This might include mode settings, symbol tables, and other details. As

여기에는 모드 설정, 기호 테이블 및 기타 세부 사항이 포함될 수 있습니다. 같이
an example, suppose that you wanted to keep track of how many NUMBER

예를 들어, 몇 개의 숫자를 추적하고 싶다고 가정합니다.
tokens had been encountered.

One way to do this is to keep a set of global variables in the module

이를 수행하는 한 가지 방법은 모듈에 일련의 글로벌 변수를 유지하는 것입니다.
where you created the lexer. For example:

Lexer를 만든 곳. 예를 들어:

    num_count = 0
    def t_NUMBER(t):
        r'\d+'
        global num_count
        num_count += 1
        t.value = int(t.value)    
        return t

If you don\'t like the use of a global variable, another place to store

글로벌 변수의 사용과 같이하지 않으면 저장할 다른 장소
information is inside the Lexer object created by `lex()`. To do this, you

정보는`lex ()`에 의해 생성 된 Lexer 객체 안에 있습니다. 이렇게하려면, 당신
can use the `lexer` attribute of tokens passed to the various rules. For

다양한 규칙에 전달 된 토큰의 '렉서'속성을 사용할 수 있습니다. 을 위한
example:

    def t_NUMBER(t):
        r'\d+'
        t.lexer.num_count += 1     # Note the use of lexer attribute

t.lexer.num_count += 1 # lexer 속성 사용 참고
        t.value = int(t.value)    
        return t

반환 t

    lexer = lex.lex()
    lexer.num_count = 0            # Set the initial count

Lexer.num_count = 0 # 초기 카운트를 설정합니다

This latter approach has the advantage of being simple and working

이 후자의 접근 방식은 단순하고 작동한다는 이점이 있습니다.
correctly in applications where multiple instantiations of a given lexer

주어진 Lexer의 여러 인스턴스화가있는 응용 프로그램에서 올바르게
exist in the same application. However, this might also feel like a

동일한 응용 프로그램에 존재합니다. 그러나 이것은 또한 같은 느낌이들 수도 있습니다
gross violation of encapsulation to OO purists. Just to put your mind at

OO 순수 주의자에 대한 캡슐화의 총 위반. 당신의 마음을두기 위해
some ease, all internal attributes of the lexer (with the exception of

Lexer의 모든 내부 속성 (제외)
`lineno`) have names that are prefixed by `lex` (e.g.,

`lineno`)는`lex`에 의해 접두사가있는 이름이 있습니다 (예 :
`lexdata`, `lexpos`, etc.). Thus, it is perfectly safe to store

`lexdata`,`lexpos '등). 따라서 저장하는 것이 안전합니다
attributes in the lexer that don\'t have names starting with that prefix

Lexer의 속성은 그 접두사로 시작하는 이름을 가지고 있습니다.
or a name that conflicts with one of the predefined methods (e.g.,

또는 사전 정의 된 방법 중 하나와 충돌하는 이름 (예 :
`input()`, `token()`, etc.).

If you don\'t like assigning values on the lexer object, you can define

Lexer 객체에 값을 할당하는 것을 좋아하지 않으면 정의 할 수 있습니다.
your lexer as a class as shown in the previous section:

이전 섹션에서 볼 수 있듯이 클래스로서의 Lexer :

    class MyLexer:
        ...
        def t_NUMBER(self,t):
            r'\d+'
            self.num_count += 1

self.num_count += 1
            t.value = int(t.value)    
            return t

        def build(self, **kwargs):
            self.lexer = lex.lex(object=self,**kwargs)

self.lexer = lex.lex (object = self, ** kwargs)
        def __init__(self):
            self.num_count = 0

self.num_count = 0

The class approach may be the easiest to manage if your application is

클래스 접근 방식은 응용 프로그램이있는 경우 관리하기가 가장 쉬울 수 있습니다.
going to be creating multiple instances of the same lexer and you need

동일한 Lexer의 여러 인스턴스를 만들고 필요합니다.
to manage a lot of state.

많은 상태를 관리합니다.

State can also be managed through closures. For example:

상태는 폐쇄를 통해 관리 할 수도 있습니다. 예를 들어:

    def MyLexer():
        num_count = 0

        num_count = 0
        ...
        def t_NUMBER(t):
            r'\d+'
            nonlocal num_count

비 로컬 NUM_COUNT
            num_count += 1
            t.value = int(t.value)    
            return t
        ...

### Lexer cloning

### Lexer 클로닝

If necessary, a lexer object can be duplicated by invoking its `clone()`

필요한 경우`Clone ()`를 호출하여 Lexer 객체를 복제 할 수 있습니다.
method. For example:

방법. 예를 들어:

    lexer = lex.lex()
    ...
    newlexer = lexer.clone()

When a lexer is cloned, the copy is exactly identical to the original

Lexer가 복제되면 사본은 원본과 정확히 동일합니다.
lexer including any input text and internal state. However, the clone

입력 텍스트 및 내부 상태를 포함한 Lexer. 그러나 클론
allows a different set of input text to be supplied which may be

다른 입력 텍스트 세트를 제공 할 수 있습니다.
processed separately. This may be useful in situations when you are

별도로 처리됩니다. 이것은 당신이있을 때 상황에 유용 할 수 있습니다
writing a parser/compiler that involves recursive or reentrant

재귀 또는 재진매와 관련된 파서/컴파일러 작성
processing. For instance, if you needed to scan ahead in the input for

처리. 예를 들어, 입력에서 미리 스캔 해야하는 경우
some reason, you could create a clone and use it to look ahead. Or, if

어떤 이유로, 당신은 클론을 만들고 그것을 사용할 수 있습니다. 또는 if
you were implementing some kind of preprocessor, cloned lexers could be

당신은 일종의 사전 처리기를 구현하고 있었고, 복제 된 Lexers는
used to handle different input files.

다른 입력 파일을 처리하는 데 사용됩니다.

Creating a clone is different than calling `lex.lex()` in that PLY

클론을 만드는 것은`lex.lex ()`를 호출하는 것과 다릅니다.
doesn\'t regenerate any of the internal tables or regular expressions.

내부 테이블이나 정규 표현식을 재생하지 않습니다.

Special considerations need to be made when cloning lexers that also

Lexers를 복제 할 때 특별한 고려 사항을 작성해야합니다.
maintain their own internal state using classes or closures. Namely, you

클래스 또는 클래스를 사용하여 자신의 내부 상태를 유지하십시오. 즉, 당신
need to be aware that the newly created lexers will share all of this

새로 만든 Lexers 가이 모든 것을 공유 할 것임을 알고 있어야합니다.
state with the original lexer. For example, if you defined a lexer as a

원래 Lexer와 함께 상태. 예를 들어, Lexer를
class and did this:

수업과 이것을했습니다 :

    m = MyLexer()
    a = lex.lex(object=m)      # Create a lexer

    b = a.clone()              # Clone the lexer

B = A.Clone () # Lexer를 복제합니다

Then both `a` and `b` are going to be bound to the same object `m` and

그러면`a`와`b`는 모두 같은 개체`m`과 함께 묶여 있고
any changes to `m` will be reflected in both lexers. It\'s important to

`m`에 대한 변경 사항은 두 Lexers에 반영됩니다. 그것은 중요합니다
emphasize that `clone()` is only meant to create a new lexer that reuses

`clone ()`는 재사용하는 새로운 렉서를 만드는 것만 강조합니다.
the regular expressions and the environment of another lexer. If you need to

다른 렉서의 정규 표현과 환경. 필요한 경우
make a totally new copy of a lexer, then call `lex()` again.

Lexer의 완전히 새로운 사본을 만든 다음`lex ()`을 다시 전화하십시오.

### Internal lexer state

### Internal lexer state

A Lexer object `lexer` has a number of internal attributes that may be

Lexer Object`Lexer`에는 여러 가지 내부 속성이 있습니다.
useful in certain situations:

특정 상황에서 유용 :

`lexer.lexpos`

:   This attribute is an integer that contains the current position

:이 속성은 현재 위치를 포함하는 정수입니다.
    within the input text. If you modify the value, it will change the

입력 텍스트 내에서. 값을 수정하면 변경됩니다.
    result of the next call to `token()`. Within token rule functions,

`token ()`에 대한 다음 호출 결과. 토큰 규칙 기능 내에서
    this points to the first character *after* the matched text. If the

이것은 일치하는 텍스트 후 첫 번째 문자 *를 가리 킵니다. 만약
    value is modified within a rule, the next returned token will be

값은 규칙 내에서 수정되며 다음 반환 된 토큰은 다음과 같습니다.
    matched at the new position.

새로운 직책에서 일치합니다.

`lexer.lineno`

:   The current value of the line number attribute stored in the lexer.

: Lexer에 저장된 줄 번호 속성의 현재 값.
    PLY only specifies that the attribute exists\-\--it never sets,

ply는 속성이 \-\ 존재한다는 것을 지정합니다.
    updates, or performs any processing with it. If you want to track

업데이트하거나 처리하는 작업을 수행합니다. 당신이 추적하고 싶다면
    line numbers, you will need to add code yourself (see the section on

줄 번호, 직접 코드를 추가해야합니다 (섹션 참조
    line numbers and positional information).

줄 번호 및 위치 정보).

`lexer.lexdata`

:   The current input text stored in the lexer. This is the string

: Lexer에 저장된 현재 입력 텍스트. 이것은 문자열입니다
    passed with the `input()` method. It would probably be a bad idea to

`input ()`메소드로 통과했습니다. 아마도 나쁜 생각 일 것입니다
    modify this unless you really know what you\'re doing.

당신이 무엇을하는지 실제로 알지 못하면 이것을 수정하십시오.

`lexer.lexmatch`

:   This is the raw `Match` object returned by the Python `re.match()`

: 이것은 Python` re.match ()`에 의해 반환 된 Raw` 매치 '객체입니다.
    function (used internally by PLY) for the current token. If you have

현재 토큰의 기능 (Ply가 내부적으로 사용). 당신이 가지고 있다면
    written a regular expression that contains named groups, you can use

명명 된 그룹이 포함 된 정규 표현을 작성하면 사용할 수 있습니다.
    this to retrieve those values.

이것은 해당 값을 검색합니다.
	Note: This attribute is only updated when tokens are defined and processed by functions.

참고 :이 속성은 토큰이 함수에 의해 정의되고 처리 될 때만 업데이트됩니다.

### Conditional lexing and start conditions

### 조건부 렉싱 및 시작 조건

In advanced parsing applications, it may be useful to have different

고급 구문 분석 응용 프로그램에서는 다르게 사용하는 것이 유용 할 수 있습니다.
lexing states. For instance, you may want the occurrence of a certain

렉싱 상태. 예를 들어, 특정 발생을 원할 수 있습니다.
token or syntactic construct to trigger a different kind of lexing. PLY

다른 종류의 렉싱을 트리거하기 위해 토큰 또는 구문 구성. 주름
supports a feature that allows the underlying lexer to be put into a

기본 Lexer를
series of different states. Each state can have its own tokens, lexing

일련의 다른 상태. 각 주에는 자체 토큰, 렉싱이있을 수 있습니다
rules, and so forth. The implementation is based largely on the \"start

규칙 등. 구현은 주로 \ "시작에 기반을두고 있습니다.
condition\" feature of GNU flex. Details of this can be found at

조건 \ "GNU Flex의 기능. 이에 대한 세부 사항은 다음에서 찾을 수 있습니다.
<https://westes.github.io/flex/manual/Start-Conditions.html>

To define a new lexing state, it must first be declared. This is done by

새로운 Lexing 상태를 정의하려면 먼저 선언해야합니다. 이것은 이에 의해 수행됩니다
including a \"states\" declaration in your lex file. For example:

lex 파일에 \ "상태 \"선언을 포함합니다. 예를 들어:

    states = (

    states = (
       ('foo','exclusive'),

( 'foo', '독점'),
       ('bar','inclusive'),

( '바', '포함'),
    )

This declaration declares two states, `'foo'` and `'bar'`. States may be

이 선언은``foo ''와` 'bar' '라는 두 가지 주를 선언합니다. 상태 일 수 있습니다
of two types; `'exclusive'` and `'inclusive'`. An ``'exclusive'`` state

두 가지 유형의; ``독점 '및`'포함 '. ```독점 ''상태
completely overrides the default behavior of the lexer. That is, lex

Lexer의 기본 동작을 완전히 무시합니다. 즉, Lex입니다
will only return tokens and apply rules defined specifically for that

토큰 만 반환하고 특별히 정의 된 규칙을 적용합니다.
state. An ``'inclusive'`` state adds additional tokens and rules to the

상태. ``포용 적 ''상태는 추가 토큰과 규칙을 추가합니다.
default set of rules. Thus, lex will return both the tokens defined by

기본 규칙 세트. 따라서 Lex는
default in addition to those defined for the ``'inclusive'`` state.

기본값``포용 적 ''상태에 정의 된 것 외에도 기본값.

Once a state has been declared, tokens and rules are declared by

주가 선언되면 토큰과 규칙이 선언됩니다.
including the state name in token/rule declaration. For example:

토큰/규칙 선언에 상태 이름을 포함합니다. 예를 들어:

    t_foo_NUMBER = r'\d+'                      # Token 'NUMBER' in state 'foo'        

t_foo_number = r '\ d+' # token 'numben'in State 'Football'
    t_bar_ID     = r'[a-zA-Z_][a-zA-Z0-9_]*'   # Token 'ID' in state 'bar'

t_bar_id = r '[a-za-z _] [a-za-z0-9 _]*' # token 'id'state 'bar'

    def t_foo_newline(t):

def t_foo_newline (t) :
        r'\n'
        t.lexer.lineno += 1

A token can be declared in multiple states by including multiple state

여러 상태를 포함하여 여러 상태에서 토큰을 선언 할 수 있습니다.
names in the declaration. For example:

선언의 이름. 예를 들어:

    t_foo_bar_NUMBER = r'\d+'         # Defines token 'NUMBER' in both state 'foo' and 'bar'

t_foo_bar_number = r '\ d+' # State 'foo'및 'bar'모두에서 토큰 '번호'를 정의합니다.

Alternative, a token can be declared in all states using the \'ANY\' in

대안, 토큰은 모든 주에서 \ 'any \'in을 사용하여 선언 할 수 있습니다.
the name:

이름:

    t_ANY_NUMBER = r'\d+'         # Defines a token 'NUMBER' in all states

t_any_number = r '\ d+' # 모든 주에서 토큰 '번호'를 정의합니다.

If no state name is supplied, as is normally the case, the token is

상태 이름이 제공되지 않으면 일반적으로 그렇듯이 토큰은
associated with a special state `'INITIAL'`. For example, these two

특별한 상태` ''이니셜 '과 관련이 있습니다. 예를 들어,이 두 가지
declarations are identical:

    t_NUMBER = r'\d+'
    t_INITIAL_NUMBER = r'\d+'

States are also associated with the special `t_ignore`, `t_error()`, and

상태는 특별`t_ignore`,`t_error ()`및
`t_eof()` declarations. For example, if a state treats these

`t_eof ()`선언. 예를 들어, 상태가이를 취급하는 경우
differently, you can declare:

    t_foo_ignore = " \t\n"       # Ignored characters for state 'foo'

tfoo는 무시 = "\ tn" # State 'Food'에 대한 문자 무시 된 문자

    def t_bar_error(t):          # Special error handler for state 'bar'
        pass 

By default, lexing operates in the `'INITIAL'` state. This state

기본적으로 Lexing은` '초기' '상태에서 작동합니다. 이 상태
includes all of the normally defined tokens. For users who aren\'t using

일반적으로 정의 된 모든 토큰을 포함합니다. 사용하는 사용자를 위해
different states, this fact is completely transparent. If, during lexing

다른 상태,이 사실은 완전히 투명합니다. 렉싱 중에
or parsing, you want to change the lexing state, use the `begin()`

또는 구문 분석, Lexing 상태를 변경하고`begin ()`를 사용합니다.
method. For example:

방법. 예를 들어:

    def t_begin_foo(t):
        r'start_foo'

r'start_foo '
        t.lexer.begin('foo')             # Starts 'foo' state

t.lexer.begin ( 'foo') # 시작 'foo'state 시작

To get out of a state, you use `begin()` to switch back to the initial

상태에서 벗어나려면`begin ()`를 사용하여 초기로 다시 전환합니다.
state. For example:

    def t_foo_end(t):
        r'end_foo'
        t.lexer.begin('INITIAL')        # Back to the initial state

t.lexer.begin ( 'Initial') # 초기 상태로 돌아 가기

The management of states can also be done with a stack. For example:

상태 관리는 스택으로 수행 할 수도 있습니다. 예를 들어:

    def t_begin_foo(t):
        r'start_foo'

r'start_foo '
        t.lexer.push_state('foo')             # Starts 'foo' state

t.lexer.push_state ( 'foo') # 'foo'state 시작

    def t_foo_end(t):
        r'end_foo'
        t.lexer.pop_state()                   # Back to the previous state

t.lexer.pop_state () # 이전 상태로 돌아갑니다

The use of a stack would be useful in situations where there are many

스택을 사용하는 것은 많은 사람들이있는 상황에 유용합니다.
ways of entering a new lexing state and you merely want to go back to

새로운 Lexing State에 들어가는 방법과 당신은 단지 다시 돌아가고 싶어합니다.
the previous state afterwards.

나중에 이전 상태.

An example might help clarify. Suppose you were writing a parser and you

예를 들어 명확히하는 데 도움이 될 수 있습니다. 당신이 파서와 당신을 쓰고 있다고 가정 해 봅시다
wanted to grab sections of arbitrary C code enclosed by curly braces.

Curly Braces로 둘러싸인 임의의 C 코드의 섹션을 잡고 싶었습니다.
That is, whenever you encounter a starting brace ``{``, you want to read

즉, 시작 브레이스가 닿을 때마다`{``, 당신은 읽고 싶습니다.
all of the enclosed code up to the ending brace ``}`` and return it as a

엔딩 브레이스까지의 모든 밀폐 된 코드``}`````
string. Doing this with a normal regular expression rule is nearly (if

끈. 정상적인 정규 표현 규칙으로 이것을하는 것은 거의 (
not actually) impossible. This is because braces can be nested and can

실제로) 불가능합니다. 버팀대가 중첩 될 수 있기 때문입니다
be included in comments and strings. Thus, matching up to the first

주석과 문자열에 포함됩니다. 따라서 첫 번째와 일치합니다
matching ``}`` character isn\'t good enough. Here is how you might use

``}``캐릭터와 일치하는 것은 충분하지 않습니다. 다음은 사용할 수있는 방법입니다
lexer states to do this:

Lexer는 다음을 수행 할 수 있습니다.

	import ply.lex as lex

ply.lex를 lex로 가져옵니다

	# Declare the states

# 주를 선언합니다
    states = (
      ('ccode','exclusive'),
    )

    # Match the first '{' Enter ccode state.

# 첫 번째 '{'입력 상태와 일치합니다.
    def t_ccode(t):
        r'\{'
        t.lexer.code_start = t.lexer.lexpos        # Record the starting position

t.lexer.code_start = t.lexer.lexpos # 시작 위치를 기록합니다
        t.lexer.level = 1                          # Initial brace level
        t.lexer.begin('ccode')                     # Enter 'ccode' state

    # Rules for the 'ccode' state

# 'ccode'상태에 대한 규칙
    def t_ccode_lbrace(t):     
        r'\{'
        t.lexer.level += 1                

    def t_ccode_rbrace(t):
        r'\}'
        t.lexer.level -= 1

        # If closing brace, return the code fragment

# 브레이스를 닫으면 코드 조각을 반환하십시오
        if t.lexer.level == 0:
             t.value = t.lexer.lexdata[t.lexer.code_start:t.lexer.lexpos+1]
             t.type = "CCODE"

t.type = "코드"
             t.lexer.lineno += t.value.count('\n')
             t.lexer.begin('INITIAL')           

t.lexer.begin ( '초기')
             return t

반환 t

    # C or C++ comment (ignore)    
    def t_ccode_comment(t):
        r'(/\*(.|\n)*?\*/)|(//.*)'
        pass

    # C string

# C 문자열
    def t_ccode_string(t):

def t_ccode_string (t) :
       r'\"([^\\\n]|(\\.))*?\"'

    # C character literal

# c 캐릭터 문자
    def t_ccode_char(t):
       r'\'([^\\\n]|(\\.))*?\''

    # Any sequence of non-whitespace characters (not braces, strings)

# whitesce가 아닌 문자 순서 (중괄호, 문자열이 아님)
    def t_ccode_nonspace(t):
       r'[^\s\{\}\'\"]+'

    # Ignored characters (whitespace)

# 무시 된 문자 (공백)
    t_ccode_ignore = " \t\n"

    # For bad characters, we just skip over it

# 나쁜 캐릭터의 경우, 우리는 그냥 건너 뜁니다.
    def t_ccode_error(t):
        t.lexer.skip(1)
	
	lexer = lex.lex()
    data = "{}"

    lexer.input(data)
    while True:

사실이지만 :
        tok = lexer.token()
        if not tok:

토크가 아닌 경우 :
            break
        print(tok)


In this example, the occurrence of the first ``{`` causes the lexer to

이 예에서, 첫 번째``{```````` ''의 발생은 Lexer가
record the starting position and enter a new state `'ccode'`. A

시작 위치를 기록하고 새 상태` 'CCODE'를 입력하십시오. ㅏ
collection of rules then match various parts of the input that follow

규칙 수집은 다음 입력의 다양한 부분과 일치합니다.
(comments, strings, etc.). All of these rules merely discard the token

(주석, 문자열 등). 이 모든 규칙은 단지 토큰을 버립니다
(by not returning a value). However, if the closing right brace is

(값을 반환하지 않음). 그러나 닫는 오른쪽 버팀대가있는 경우
encountered, the rule `t_ccode_rbrace` collects all of the code (using

발생하는 규칙`t_ccode_rbrace`는 모든 코드를 수집합니다 (사용
the earlier recorded starting position), stores it, and returns a token

이전에 기록 된 시작 위치)), 저장하고 토큰을 반환합니다.
\'CCODE\' containing all of that text. When returning the token, the

\ 'ccode \'모든 텍스트를 포함합니다. 토큰을 반환 할 때
lexing state is restored back to its initial state.

Lexing State는 초기 상태로 다시 복원됩니다.

### Miscellaneous Issues

-   The lexer requires input to be supplied as a single input string.

- Lexer는 입력을 단일 입력 문자열로 제공해야합니다.
    Since most machines have more than enough memory, this rarely

대부분의 기계에는 충분한 메모리가 있기 때문에 거의
    presents a performance concern. However, it means that the lexer

성능 문제를 제시합니다. 그러나 그것은 Lexer를 의미합니다
    currently can\'t be used with streaming data such as open files or

현재 열린 파일 또는
    sockets. This limitation is primarily a side-effect of using the

소켓. 이 제한은 주로 사용의 부작용입니다
    `re` module. You might be able to work around this by implementing

`re` 모듈. 당신은 구현하여 이것을 해결할 수 있습니다.
    an appropriate `def t_eof()` end-of-file handling rule. The main

적절한`def t_eof ()`파일 끝 처리 규칙. 메인
    complication here is that you\'ll probably need to ensure that data

여기서 합병증은 당신이 아마도 그 데이터를 보장해야한다는 것입니다.
    is fed to the lexer in a way so that it doesn\'t split in the

렉서에게 공급되어
    middle of a token.

토큰의 중간.

-   If you need to supply optional flags to the ``re.compile()`` function,

-``re.compile ()``function,``re.compile ()`
    supply the ``reflags`` option to lex. For example:

Lex에``reflegs`` 옵션을 제공하십시오. 예를 들어:

        lex.lex(reflags=re.UNICODE | re.VERBOSE)

    Note: by default, `reflags` is set to `re.VERBOSE`. If you provide

참고 : 기본적으로`reflags`는`re.verbose`로 설정됩니다. 당신이 제공하는 경우
    your own flags, you may need to include this for PLY to preserve its

자신의 깃발, Ply를 보존하려면 이것을 포함시켜야 할 수도 있습니다.
    normal behavior.

정상적인 행동.
-   If you are going to create a hand-written lexer and you plan to use

- 손으로 쓴 렉서를 만들고 사용할 계획이라면
    it with `yacc.py`, it only needs to conform to the following

`yacc.py`와 함께, 다음과 일치하면됩니다.
    requirements:

    1.  It must provide a `token()` method that returns the next token

1. 다음 토큰을 반환하는`token ()`메소드를 제공해야합니다.
        or `None` if no more tokens are available.
    2.  The `token()` method must return an object `tok` that has `type`

2.`token ()`메소드는`type`가있는 객체`tok`를 반환해야합니다.
        and `value` attributes. If line number tracking is being used,

그리고 'value'속성. 라인 번호 추적이 사용되는 경우
        then the token should also define a `lineno` attribute.

그런 다음 토큰은 또한`lineno '속성을 정의해야합니다.

## Parsing basics

## 구문 분석 기본

`yacc.py` is used to parse language syntax. Before showing an example,

`yacc.py`는 언어 구문을 구문 분석하는 데 사용됩니다. 예를 보여주기 전에
there are a few important bits of background that must be mentioned.

언급해야 할 몇 가지 중요한 배경이 있습니다.
First, *syntax* is usually specified in terms of a BNF grammar. For

첫째, * 구문 *은 일반적으로 BNF 문법 측면에서 지정됩니다. 을 위한
example, if you wanted to parse simple arithmetic expressions, you might

예를 들어 간단한 산술 표현을 구문 분석하고 싶다면
first write an unambiguous grammar specification like this:

먼저 다음과 같은 명백한 문법 사양을 작성하십시오.

    expression : expression + term
               | expression - term

| 표현 - 용어
               | term

    term       : term * factor

용어 : 용어 * 요인
               | term / factor

| 용어 / 요인
               | factor

| 요인

    factor     : NUMBER

요인 : 숫자
               | ( expression )

In the grammar, symbols such as `NUMBER`, `+`, `-`, `*`, and `/` are

문법에서`number`,`+`,`-`,`및`/`와 같은 기호는
known as *terminals* and correspond to input tokens. Identifiers such as

* 터미널 *로 알려져 있으며 입력 토큰에 해당합니다. 다음과 같은 식별자
`term` and `factor` refer to grammar rules comprised of a collection of

`용어 '및`accor'는
terminals and other rules. These identifiers are known as

터미널 및 기타 규칙. 이 식별자는 다음으로 알려져 있습니다
*non-terminals*.

*비 터미널*.

The semantic behavior of a language is often specified using a technique

언어의 의미 론적 행동은 종종 기술을 사용하여 지정됩니다.
known as syntax directed translation. In syntax directed translation,

구문 지시 된 번역으로 알려져 있습니다. 구문 지시 된 번역에서
attributes are attached to each symbol in a given grammar rule along

속성은 주어진 문법 규칙으로 각 기호에 첨부됩니다.
with an action. Whenever a particular grammar rule is recognized, the

행동으로. 특정 문법 규칙이 인식 될 때마다
action describes what to do. For example, given the expression grammar

행동은해야 할 일을 설명합니다. 예를 들어, 표현 문법이 주어지면
above, you might write the specification for a simple calculator like

위의 경우 간단한 계산기와 같은 사양을 작성할 수 있습니다.
this:

이것:

    Grammar                             Action

문법 작용
    --------------------------------    -------------------------------------------- 
    expression0 : expression1 + term    expression0.val = expression1.val + term.val
                | expression1 - term    expression0.val = expression1.val - term.val
                | term                  expression0.val = term.val

    term0       : term1 * factor        term0.val = term1.val * factor.val

term0 : term1 * 요인 용어 0.val = term1.val * factor.val
                | term1 / factor        term0.val = term1.val / factor.val

| 용어 1 / 계수 용어 0.Val = term1.val / factor.val
                | factor                term0.val = factor.val

| 계수 term0.val = factor.val

    factor      : NUMBER                factor.val = int(NUMBER.lexval)

요인 : 숫자 계수 .Val = int (number.lexval)
                | ( expression )        factor.val = expression.val

A good way to think about syntax directed translation is to view each

구문 지시 된 번역에 대해 생각하는 좋은 방법은 각각을 보는 것입니다.
symbol in the grammar as a kind of object. Associated with each symbol

문법의 상징은 일종의 물체로서. 각 기호와 관련이 있습니다
is a value representing its \"state\" (for example, the `val` attribute

\ "State \"를 나타내는 값입니다 (예 :`val` 속성
above). Semantic actions are then expressed as a collection of functions

위에). 시맨틱 동작은 기능 모음으로 표현됩니다.
or methods that operate on the symbols and associated values.

또는 기호 및 관련 값에서 작동하는 메소드.

Yacc uses a parsing technique known as LR-parsing or shift-reduce

YACC
parsing. LR parsing is a bottom up technique that tries to recognize the

구문 분석. LR 파싱은
right-hand-side of various grammar rules. Whenever a valid

다양한 문법 규칙의 오른쪽. 유효 할 때마다
right-hand-side is found in the input, the appropriate action code is

오른쪽은 입력에서 발견되며 적절한 조치 코드는 다음과 같습니다.
triggered and the grammar symbols are replaced by the grammar symbol on

트리거되고 문법 기호는 문법 기호로 대체됩니다.
the left-hand-side.

왼쪽.

LR parsing is commonly implemented by shifting grammar symbols onto a

LR 파싱은 일반적으로 문법 기호를
stack and looking at the stack and the next input token for patterns

스택 및 패턴에 대한 스택 및 다음 입력 토큰을 봅니다.
that match one of the grammar rules. The details of the algorithm can be

그것은 문법 규칙 중 하나와 일치합니다. 알고리즘의 세부 사항은 다음과 같습니다
found in a compiler textbook, but the following example illustrates the

컴파일러 교과서에서 발견되지만 다음 예는 다음을 보여줍니다.
steps that are performed if you wanted to parse the expression

표현을 구문 분석하고 싶을 때 수행되는 단계
`3 + 5 * (10 - 20)` using the grammar defined above. In the example, the

`3 + 5 * (10-20)`위에서 정의 된 문법을 사용합니다. 예에서
special symbol `$` represents the end of input:

특수 기호`$`는 입력의 끝을 나타냅니다.

    Step Symbol Stack           Input Tokens            Action

스텝 심볼 스택 입력 토큰 동작
    ---- ---------------------  ---------------------   -------------------------------
    1                           3 + 5 * ( 10 - 20 )$    Shift 3
    2    3                        + 5 * ( 10 - 20 )$    Reduce factor : NUMBER

2 3 + 5 * (10-20) $ 축소 요인 : 숫자
    3    factor                   + 5 * ( 10 - 20 )$    Reduce term   : factor

3 요소 + 5 * (10-20) $ 단축 항 : 요인
    4    term                     + 5 * ( 10 - 20 )$    Reduce expr : term

4 기 + 5 * (10-20) $ expr : 용어
    5    expr                     + 5 * ( 10 - 20 )$    Shift +

5 Expr + 5 * (10-20) $ shift +
    6    expr +                     5 * ( 10 - 20 )$    Shift 5

6 Expr + 5 * (10-20) $ Shift 5
    7    expr + 5                     * ( 10 - 20 )$    Reduce factor : NUMBER
    8    expr + factor                * ( 10 - 20 )$    Reduce term   : factor

8 expr + factor * (10-20) $ change term : factor
    9    expr + term                  * ( 10 - 20 )$    Shift *

9 Expr + term * (10-20) $ shift *
    10   expr + term *                  ( 10 - 20 )$    Shift (

10 Expr + term * (10-20) $ shift (
    11   expr + term * (                  10 - 20 )$    Shift 10

11 Expr + term * (10-20) $ shift 10
    12   expr + term * ( 10                  - 20 )$    Reduce factor : NUMBER

12 Expr + term * (10-20) $ 축소 요인 : 숫자
    13   expr + term * ( factor              - 20 )$    Reduce term : factor

13 Expr + term * (요인 -20) $ 단축 항 : 요인
    14   expr + term * ( term                - 20 )$    Reduce expr : term

14 Expr + term * (용어 -20) $ expr : 용어
    15   expr + term * ( expr                - 20 )$    Shift -

15 expr + term * (expr -20) $ shift -
    16   expr + term * ( expr -                20 )$    Shift 20

16 Expr + term * (expr -20) $ shift 20
    17   expr + term * ( expr - 20                )$    Reduce factor : NUMBER

17 Expr + term * (expr -20) $ 축소 요인 : 숫자
    18   expr + term * ( expr - factor            )$    Reduce term : factor

18 Expr + term * (expr -factor) $ 줄인 용어 : 팩터
    19   expr + term * ( expr - term              )$    Reduce expr : expr - term
    20   expr + term * ( expr                     )$    Shift )

20 expr + term * (expr) $ shift)
    21   expr + term * ( expr )                    $    Reduce factor : (expr)
    22   expr + term * factor                      $    Reduce term : term * factor

22 expr + term * 요인 $ 축소 용어 : 용어 * 팩터
    23   expr + term                               $    Reduce expr : expr + term
    24   expr                                      $    Reduce expr
    25                                             $    Success!

25 $ 성공!

When parsing the expression, an underlying state machine and the current

표현을 구문 분석 할 때, 기본 상태 기계 및 전류
input token determine what happens next. If the next token looks like

입력 토큰은 다음에 어떤 일이 발생하는지 결정합니다. 다음 토큰이 보이는 경우
part of a valid grammar rule (based on other items on the stack), it is

유효한 문법 규칙의 일부 (스택의 다른 항목을 기반으로)
generally shifted onto the stack. If the top of the stack contains a

일반적으로 스택으로 이동했습니다. 스택의 상단에 a가 포함 된 경우
valid right-hand-side of a grammar rule, it is usually \"reduced\" and

문법 규칙의 유효한 오른쪽, 일반적으로 \ "감소 \"및
the symbols replaced with the symbol on the left-hand-side. When this

기호는 왼쪽의 기호로 대체되었습니다. 이렇게하면
reduction occurs, the appropriate action is triggered (if defined). If

감소가 발생하면 적절한 조치가 트리거됩니다 (정의 된 경우). 만약에
the input token can\'t be shifted and the top of stack doesn\'t match

입력 토큰은 이동할 수없고 스택 상단은 일치하지 않습니다.
any grammar rules, a syntax error has occurred and the parser must take

모든 문법 규칙, 구문 오류가 발생했으며 파서는
some kind of recovery step (or bail out). A parse is only successful if

일종의 회복 단계 (또는 구제). 구문 분석은 만약 만 성공합니다
the parser reaches a state where the symbol stack is empty and there are

파서는 기호 스택이 비어 있고있는 상태에 도달하고 있습니다.
no more input tokens.

It is important to note that the underlying implementation is built

기본 구현이 구축되었음을 주목하는 것이 중요합니다.
around a large finite-state machine that is encoded in a collection of

모음으로 인코딩 된 대형 유한 상태 기계 주변
tables. The construction of these tables is non-trivial and beyond the

테이블. 이 테이블의 구성은 사소한 일이며
scope of this discussion. However, subtle details of this process

이 토론의 범위. 그러나이 과정의 미묘한 세부 사항
explain why, in the example above, the parser chooses to shift a token

위의 예에서 파서가 토큰을 이동하기로 선택한 이유를 설명하십시오.
onto the stack in step 9 rather than reducing the rule

규칙을 줄이기보다는 9 단계의 스택에
`expr : expr + term`.

## Yacc

The `ply.yacc` module implements the parsing component of PLY. The name

`ply.yacc` 모듈은 Ply의 구문 분석 구성 요소를 구현합니다. 이름
\"yacc\" stands for \"Yet Another Compiler Compiler\" and is borrowed

\ "yacc \"는 \ "또 다른 컴파일러 컴파일러 \"를 나타냅니다.
from the Unix tool of the same name.

같은 이름의 유닉스 도구에서.

### An example

Suppose you wanted to make a grammar for simple arithmetic expressions

간단한 산술 표현을 위해 문법을 만들고 싶다고 가정 해 봅시다
as previously described. Here is how you would do it with `yacc.py`:

앞에서 설명한대로. 다음은`yacc.py`를 사용하여 어떻게 할 것인가입니다.

    # Yacc example

    import ply.yacc as yacc

ply.yacc를 YACC로 가져옵니다

    # Get the token map from the lexer.  This is required.

# Lexer에서 토큰 맵을받습니다. 이것은 필요합니다.
    from calclex import tokens

Calclex Import Tokens에서

    def p_expression_plus(p):
        'expression : expression PLUS term'
        p[0] = p[1] + p[3]

    def p_expression_minus(p):
        'expression : expression MINUS term'
        p[0] = p[1] - p[3]

    def p_expression_term(p):

    def p_expression_term(p):
        'expression : term'

'표현 : 용어'
        p[0] = p[1]

    def p_term_times(p):

def p_term_times (p) :
        'term : term TIMES factor'

'용어 : 용어 시간 요인'
        p[0] = p[1] * p[3]

    def p_term_div(p):
        'term : term DIVIDE factor'

'용어 : 용어 분할 요소'
        p[0] = p[1] / p[3]

    def p_term_factor(p):

def p_term_factor (p) :
        'term : factor'

'용어 : 요인'
        p[0] = p[1]

    def p_factor_num(p):
        'factor : NUMBER'

'요인 : 숫자'
        p[0] = p[1]

    def p_factor_expr(p):
        'factor : LPAREN expression RPAREN'

'요인 : LPAREN 표현 RPAREN'
        p[0] = p[2]

    # Error rule for syntax errors
    def p_error(p):
        print("Syntax error in input!")

print ( "입력의 구문 오류!")

    # Build the parser

# 파서를 구축하십시오
    parser = yacc.yacc()

    while True:

사실이지만 :
       try:

노력하다:
           s = input('calc > ')
       except EOFError:
           break
       if not s: continue
       result = parser.parse(s)
       print(result)

Note: ``calclex.py`` can be found at https://github.com/dabeaz/ply/blob/master/test/calclex.py

참고 :``calclex.py '는 https://github.com/dabeaz/ply/blob/master/test/calclex.py에서 찾을 수 있습니다.

In this example, each grammar rule is defined by a Python function where

이 예에서 각 문법 규칙은 파이썬 기능으로 정의됩니다.
the docstring to that function contains the appropriate context-free

해당 함수에 대한 문서에는 적절한 컨텍스트가 포함되어 있습니다
grammar specification. The statements that make up the function body

문법 사양. 기능 본문을 구성하는 진술
implement the semantic actions of the rule. Each function accepts a

규칙의 의미 론적 행동을 구현하십시오. 각 함수는 a를 수락합니다
single argument `p` that is a sequence containing the values of each

각각의 값을 포함하는 시퀀스 인 단일 인수`p '
grammar symbol in the corresponding rule. The values of `p[i]` are

해당 규칙의 문법 기호. `p [i]`의 값은
mapped to grammar symbols as shown here:

여기에 표시된대로 문법 기호에 매핑 :

    def p_expression_plus(p):
        'expression : expression PLUS term'
        #   ^            ^        ^    ^
        #  p[0]         p[1]     p[2] p[3]

        p[0] = p[1] + p[3]

For tokens, the \"value\" of the corresponding `p[i]` is the *same* as

토큰의 경우 해당`p [i]`의 \ "value \"는 * 동일 *입니다.
the `p.value` attribute assigned in the lexer module. For non-terminals,

Lexer 모듈에 할당 된`p.Value '속성. 비 터미널의 경우
the value is determined by whatever is placed in `p[0]` when rules are

값은 규칙이있을 때`p [0]`에 배치 된 모든 것에 의해 결정됩니다.
reduced. This value can be anything at all. However, it probably most

줄인. 이 가치는 전혀 아무것도 될 수 있습니다. 그러나 아마도 가장 많을 것입니다
common for the value to be a simple Python type, a tuple, or an

값이 간단한 파이썬 유형, 튜플 또는
instance. In this example, we are relying on the fact that the `NUMBER`

사례. 이 예에서 우리는 '번호'가 있다는 사실에 의존하고 있습니다.
token stores an integer value in its value field. All of the other rules

토큰은 가치 필드에 정수 값을 저장합니다. 다른 모든 규칙
perform various types of integer operations and propagate the result.

다양한 유형의 정수 작업을 수행하고 결과를 전파하십시오.

Note: The use of negative indices have a special meaning in

참고 : 부정적인 지수를 사용하면 특별한 의미가 있습니다.
yacc\-\--specially `p[-1]` does not have the same value as `p[3]` in

yacc \-\-특별히`p [-1]``p [3]``와 같은 값이 없습니다.
this example. Please see the section on \"Embedded Actions\" for further

이 예. 자세한 내용은 \ "Embedded Actions \"섹션을 참조하십시오.
details.

The first rule defined in the yacc specification determines the starting

YACC 사양에 정의 된 첫 번째 규칙은 시작을 결정합니다.
grammar symbol (in this case, a rule for `expression` appears first).

문법 기호 (이 경우에는`표현 '에 대한 규칙이 먼저 나타납니다).
Whenever the starting rule is reduced by the parser and no more input is

파서에 의해 시작 규칙이 줄어들고 더 이상 입력이 없을 때마다
available, parsing stops and the final value is returned (this value

사용 가능한, 구문 분석 중지 및 최종 값이 반환됩니다 (이 값
will be whatever the top-most rule placed in `p[0]`).

`p [0]`)에 가장 큰 규칙이있을 것입니다.
Note: an alternative starting symbol can be specified using the ``start`` keyword

참고 :``start ''키워드를 사용하여 대체 시작 기호를 지정할 수 있습니다.
argument to ``yacc()``.

``yacc ()``에 대한 인수.

The `p_error(p)` rule is defined to catch syntax errors. See the error

`p_error (p)`규칙은 구문 오류를 포착하도록 정의됩니다. 오류를 참조하십시오
handling section below for more detail.

자세한 내용은 아래의 핸들링 섹션입니다.

To build the parser, call the `yacc.yacc()` function. This function

파서를 구축하려면`yacc.yacc ()`함수를 호출하십시오. 이 기능
looks at the module and attempts to construct all of the LR parsing

모듈을보고 모든 LR 파싱을 구성하려고 시도합니다.
tables for the grammar you have specified.

지정된 문법 테이블.

If any errors are detected in your grammar specification, `yacc.py` will

문법 사양에서 오류가 감지되면`yacc.py` will
produce diagnostic messages and possibly raise an exception. Some of the

진단 메시지를 생성하고 예외를 제기 할 수 있습니다. 일부
errors that can be detected include:

감지 할 수있는 오류는 다음과 같습니다.

-   Duplicated function names (if more than one rule function have the

- 복제 된 함수 이름 (둘 이상의 규칙 함수가
    same name in the grammar file).

문법 파일에서 동일한 이름).
-   Shift/reduce and reduce/reduce conflicts generated by ambiguous

- 모호한 충돌을 시프트/감소 및 감소/감소/감소
    grammars.
-   Badly specified grammar rules.

- 잘못 지정된 문법 규칙.
-   Infinite recursion (rules that can never terminate).

- 무한 재귀 (종료 할 수없는 규칙).
-   Unused rules and tokens

- 사용되지 않은 규칙 및 토큰
-   Undefined rules and tokens

- 정의되지 않은 규칙 및 토큰
The next few sections discuss grammar specification in more detail.

다음 몇 섹션에서는 문법 사양에 대해 자세히 설명합니다.

The final part of the example shows how to actually run the parser

예제의 마지막 부분은 실제로 파서를 실행하는 방법을 보여줍니다.
created by `yacc()`. To run the parser, you have to call the `parse()`

`yacc ()`에 의해 만들어졌습니다. 파서를 실행하려면`parse ()`을 호출해야합니다.
with a string of input text. This will run all of the grammar rules and

입력 텍스트 문자열이 있습니다. 이것은 모든 문법 규칙을 실행합니다
return the result of the entire parse. This result return is the value

전체 구문 분석 결과를 반환하십시오. 이 결과 반환은 값입니다
assigned to `p[0]` in the starting grammar rule.

시작 문법 규칙에서`p [0]`에 할당되었습니다.

### Combining Grammar Rule Functions

### 문법 규칙 기능 결합

When grammar rules are similar, they can be combined into a single

문법 규칙이 비슷하면 단일로 결합 할 수 있습니다.
function. For example, consider the two rules in our earlier example:

기능. 예를 들어, 이전 예제에서 두 가지 규칙을 고려하십시오.

    def p_expression_plus(p):
        'expression : expression PLUS term'
        p[0] = p[1] + p[3]

    def p_expression_minus(p):
        'expression : expression MINUS term'
        p[0] = p[1] - p[3]

Instead of writing two functions, you might write a single function like

두 가지 기능을 작성하는 대신 다음과 같은 단일 기능을 작성할 수 있습니다.
this:

이것:

    def p_expression(p):
        '''expression : expression PLUS term
                      | expression MINUS term'''

| 표현 마이너스 용어 '' '
        if p[2] == '+':
            p[0] = p[1] + p[3]
        elif p[2] == '-':
            p[0] = p[1] - p[3]

In general, the docstring for any given function can contain multiple

일반적으로 특정 함수에 대한 문서화에는 여러 가지가 포함될 수 있습니다.
grammar rules. So, it would have also been legal (although possibly

문법 규칙. 그래서 그것은 또한 합법적 일 것입니다 (아마도
confusing) to write this:

혼란) 이것을 쓰기 :

    def p_binary_operators(p):

def p_binary_operators (p) :
        '''expression : expression PLUS term
                      | expression MINUS term

| 표현 마이너스 용어
           term       : term TIMES factor

용어 : 용어 시간 계수
                      | term DIVIDE factor'''

| 용어 분할 요인 '' '
        if p[2] == '+':
            p[0] = p[1] + p[3]
        elif p[2] == '-':
            p[0] = p[1] - p[3]
        elif p[2] == '*':
            p[0] = p[1] * p[3]
        elif p[2] == '/':
            p[0] = p[1] / p[3]

When combining grammar rules into a single function, it is usually a

문법 규칙을 단일 함수로 결합 할 때는 일반적으로
good idea for all of the rules to have a similar structure (e.g., the

모든 규칙에 비슷한 구조를 갖는 것이 좋습니다 (예 :
same number of terms). Otherwise, the corresponding action code may be

동일한 수의 용어). 그렇지 않으면 해당 조치 코드가 될 수 있습니다
more complicated than necessary. However, it is possible to handle

필요한 것보다 더 복잡합니다. 그러나 처리 할 수 있습니다
simple cases using ``len()``. For example:

``len ()``를 사용하는 간단한 사례. 예를 들어:

    def p_expressions(p):
        '''expression : expression MINUS expression
                      | MINUS expression'''
        if (len(p) == 4):
            p[0] = p[1] - p[3]
        elif (len(p) == 3):
            p[0] = -p[2]

If parsing performance is a concern, you should resist the urge to put

구문 분석 성과가 우려되면, 당신은
too much conditional processing into a single grammar rule as shown in

단일 문법 규칙으로 너무 많은 조건부 처리
these examples. When you add checks to see which grammar rule is being

이 예. 어떤 문법 규칙이 있는지 확인하기 위해 수표를 추가 할 때
handled, you are actually duplicating the work that the parser has

처리하면 실제로 파서가 가지고있는 작업을 복제하고 있습니다.
already performed (i.e., the parser already knows exactly what rule it

이미 수행 된 (즉, 파서는 이미 어떤 규칙을 정확히 알고 있습니다.
matched). You can eliminate this overhead by using a separate `p_rule()`

일치). 별도의`p_rule ()`를 사용 하여이 오버 헤드를 제거 할 수 있습니다.
function for each grammar rule.

각 문법 규칙에 대한 기능.

### Character Literals

### 문자 리터럴

If desired, a grammar may contain tokens defined as single character

원하는 경우 문법에는 단일 문자로 정의 된 토큰이 포함될 수 있습니다.
literals. For example:

    def p_binary_operators(p):

def p_binary_operators (p) :
        '''expression : expression '+' term
                      | expression '-' term

| 표현 '-'용어
           term       : term '*' factor

용어 : 용어 '*'요소
                      | term '/' factor'''

| 용어 '/'요소 '' '
        if p[2] == '+':
            p[0] = p[1] + p[3]
        elif p[2] == '-':
            p[0] = p[1] - p[3]
        elif p[2] == '*':
            p[0] = p[1] * p[3]
        elif p[2] == '/':
            p[0] = p[1] / p[3]

A character literal must be enclosed in quotes such as `'+'`. In

문자 문자는` '+'`와 같은 인용문으로 둘러싸여 있어야합니다. ~ 안에
addition, if literals are used, they must be declared in the

또한 리터럴을 사용하는 경우
corresponding `lex` file through the use of a special `literals`

특수`lygrals '를 사용하여 해당`lex` 파일
declaration:

    # Literals should be placed in module given to lex()

# 리터럴은 lex ()에 주어진 모듈에 배치해야합니다.
    literals = ['+','-','*','/']
Note: make sure that you don't have a duplicate token rule defined like `t_...` to make it work.

참고 :`t _...`와 같이 정의 된 중복 토큰 규칙이 없어야합니다.

Character literals are limited to a single character. Thus, it is not

캐릭터 리터럴은 단일 문자로 제한됩니다. 따라서 그렇지 않습니다
legal to specify literals such as ``<=`` or ``==``. For this, use the

``<=```또는``==``와 같은 리터럴을 지정하는 것이 합법적입니다. 이를 위해 사용하십시오
normal lexing rules (e.g., define a rule such as `t_EQ = r'=='`).

정상 Lexing 규칙 (예 :`t_eq = r '=='`과 같은 규칙을 정의합니다).
### Empty Productions

### 빈 프로덕션

`yacc.py` can handle empty productions by defining a rule like this:

`yacc.py '는 다음과 같은 규칙을 정의하여 빈 프로덕션을 처리 할 수 있습니다.

    def p_empty(p):

def p_empty (p) :
        'empty :'

'비어 있는 :'
        pass

Now to use the empty production, use ``empty`` as a symbol. For example:

이제 빈 생산을 사용하려면``빈 ''을 기호로 사용하십시오. 예를 들어:

    def p_optitem(p):
        'optitem : item'
        '        | empty'

'| 비어 있는'
        ...

Note: You can write empty rules anywhere by specifying an empty right

참고 : 빈 오른쪽을 지정하여 빈 규칙을 쓸 수 있습니다.
hand side. However, I personally find that writing an \"empty\" rule and

손잡이. 그러나 나는 개인적으로 "빈 \"규칙을 작성하고
using \"empty\" to denote an empty production is easier to read and more

\ "빈 \"를 사용하여 빈 생산을 표시하는 것이 더 쉽습니다.
clearly states your intentions.

당신의 의도를 명확하게 말합니다.

### Changing the starting symbol

### 시작 기호 변경

Normally, the first rule found in a yacc specification defines the

일반적으로 YACC 사양에서 발견 된 첫 번째 규칙은 다음을 정의합니다.
starting grammar rule (top level rule). To change this, supply a `start`

시작 문법 규칙 (최상위 규칙). 이것을 변경하려면 '시작'을 공급하십시오
specifier in your file. For example:

파일의 지정자. 예를 들어:

    start = 'foo'

시작 = 'foo'

    def p_bar(p):
        'bar : A B'

    # This is the starting rule due to the start specifier above

# 위의 시작 지정자로 인한 시작 규칙입니다.
    def p_foo(p):

def p_foo (p) :
        'foo : bar X'
    ...

The use of a `start` specifier may be useful during debugging since you

`start '지정자를 사용하면 디버깅 중에 유용 할 수 있습니다.
can use it to have yacc build a subset of a larger grammar. For this

YACC가 더 큰 문법의 서브 세트를 만들도록 사용할 수 있습니다. 이것을 위해
purpose, it is also possible to specify a starting symbol as an argument

목적, 시작 기호를 인수로 지정할 수도 있습니다.
to `yacc()`. For example:

`yacc ()`. 예를 들어:

    parser = yacc.yacc(start='foo')

parser = yacc.yacc (start = 'foo')

### Dealing With Ambiguous Grammars

### 모호한 문법을 다루는 것

The expression grammar given in the earlier example has been written in

이전 예제에 주어진 표현 문법은
a special format to eliminate ambiguity. However, in many situations, it

모호성을 제거하기위한 특별한 형식. 그러나 많은 상황에서
is extremely difficult or awkward to write grammars in this format. A

이 형식으로 문법을 작성하기에는 매우 어렵거나 어색합니다. ㅏ
much more natural way to express the grammar is in a more compact form

문법을 표현하는 훨씬 더 자연스러운 방법은 더 컴팩트 한 형태입니다.
like this:

    expression : expression PLUS expression
               | expression MINUS expression
               | expression TIMES expression
               | expression DIVIDE expression
               | LPAREN expression RPAREN
               | NUMBER

Unfortunately, this grammar specification is ambiguous. For example, if

불행히도,이 문법 사양은 모호합니다. 예를 들어, if
you are parsing the string \"3 \* 4 + 5\", there is no way to tell how

당신은 문자열을 구문 분석하고 있습니다 \ "3 \* 4 + 5 \"
the operators are supposed to be grouped. For example, does the

운영자는 그룹화되어야합니다. 예를 들어
expression mean \"(3 \* 4) + 5\" or is it \"3 \* (4+5)\"?

표현 평균 \ "(3 \* 4) + 5 \"또는 \ "3 \* (4 + 5) \"입니까?

When an ambiguous grammar is given to `yacc.py` it will print messages

`yacc.py '에 모호한 문법이 주어지면 메시지가 인쇄됩니다.
about \"shift/reduce conflicts\" or \"reduce/reduce conflicts\". A

약 \ "교대/갈등을 줄이기/"또는 \ "충돌 감소/감소 \". ㅏ
shift/reduce conflict is caused when the parser generator can\'t decide

파서 생성기가 결정할 때 교대/감소 충돌이 발생합니다.
whether or not to reduce a rule or shift a symbol on the parsing stack.

규칙을 줄이든 아니든, 구문 분석 스택의 기호를 이동할 것인지의 여부.
For example, consider the string \"3 \* 4 + 5\" and the internal parsing

예를 들어, 문자열 \ "3 \* 4 + 5 \"및 내부 구문 분석을 고려하십시오.
stack:

    Step Symbol Stack           Input Tokens            Action

스텝 심볼 스택 입력 토큰 동작
    ---- ---------------------  ---------------------   -------------------------------
    1    $                                3 * 4 + 5$    Shift 3
    2    $ 3                                * 4 + 5$    Reduce : expression : NUMBER

2 $ 3 * 4 + 5 $ 축소 : 표현 : 숫자
    3    $ expr                             * 4 + 5$    Shift *

3 $ expr * 4 + 5 $ shift *
    4    $ expr *                             4 + 5$    Shift 4

4 $ expr * 4 + 5 $ shift 4
    5    $ expr * 4                             + 5$    Reduce: expression : NUMBER
    6    $ expr * expr                          + 5$    SHIFT/REDUCE CONFLICT ????

In this case, when the parser reaches step 6, it has two options. One is

이 경우, 파서가 6 단계에 도달하면 두 가지 옵션이 있습니다. 하나는
to reduce the rule `expr : expr * expr` on the stack. The other option

스택에서 규칙`expr : expr * expr`을 줄입니다. 다른 옵션
is to shift the token `+` on the stack. Both options are perfectly legal

스택에서 토큰`+`을 이동하는 것입니다. 두 옵션 모두 완벽하게 합법적입니다
from the rules of the context-free-grammar.

상황이없는 문법의 규칙에서.

By default, all shift/reduce conflicts are resolved in favor of

기본적으로 모든 시프트/감소 충돌은
shifting. Therefore, in the above example, the parser will always shift

이동. 따라서 위의 예에서는 파서가 항상 이동합니다.
the `+` instead of reducing. Although this strategy works in many cases

감소하는 대신`+`. 이 전략은 많은 경우에 작동하지만
(for example, the case of \"if-then\" versus \"if-then-else\"), it is

(예를 들어, \ "if-then \"대 \ "if-then-else \"의 경우)
not enough for arithmetic expressions. In fact, in the above example,

산술 표현에는 충분하지 않습니다. 실제로 위의 예에서
the decision to shift `+` is completely wrong\-\--we should have reduced

`+`을 이동하기로 한 결정은 완전히 잘못되었습니다 \-\-우리는 감소해야합니다.
`expr * expr` since multiplication has higher mathematical precedence

``expr * expr` 곱셈이 더 높은 수학적 우선 순위가 높기 때문에`expr * expr`
than addition.

추가보다.

To resolve ambiguity, especially in expression grammars, `yacc.py`

특히 발현 문법에서 모호성을 해결하기 위해`yacc.py`
allows individual tokens to be assigned a precedence level and

개별 토큰이 우선 순위 레벨을 할당하고
associativity. This is done by adding a variable `precedence` to the

연관성. 이것은 '우선 순위'를 다음에 추가하여 수행됩니다.
grammar file like this:

    precedence = (
        ('left', 'PLUS', 'MINUS'),
        ('left', 'TIMES', 'DIVIDE'),
    )

This declaration specifies that `PLUS`/`MINUS` have the same precedence

이 선언은`plus`/`minus`가 동일한 우선 순위를 갖도록 지정합니다.
level and are left-associative and that `TIMES`/`DIVIDE` have the same

레벨과 좌측 관련이 있으며`times`/`divide`는 동일합니다.
precedence and are left-associative. Within the `precedence`

우선 순위와 왼쪽 관련성입니다. `procedence '내에서
declaration, tokens are ordered from lowest to highest precedence. Thus,

선언, 토큰은 최저에서 가장 높은 우선 순위에서 주문됩니다. 따라서,
this declaration specifies that `TIMES`/`DIVIDE` have higher precedence

이 선언은`times`/`divide`가 더 높은 우선 순위를 가지고 있음을 지정합니다.
than `PLUS`/`MINUS` (since they appear later in the precedence

`plus`/`minus '보다 (나중에 나중에 나타나기 때문에
specification).

사양).
The precedence specification works by associating a numerical precedence

우선 순위 사양은 수치 우선 순위를 연관시킴으로써 작동합니다
level value and associativity direction to the listed tokens. For

상장 된 토큰에 대한 레벨 값과 연관 방향. 을 위한
example, in the above example you will get:

예를 들어 위의 예에서는 다음과 같습니다.

    PLUS      : level = 1,  assoc = 'left'

    PLUS      : level = 1,  assoc = 'left'
    MINUS     : level = 1,  assoc = 'left'
    TIMES     : level = 2,  assoc = 'left'

시간 : 레벨 = 2, assoc = '왼쪽'
    DIVIDE    : level = 2,  assoc = 'left'

나누기 : 레벨 = 2, assoc = '왼쪽'

These values are then used to attach a numerical precedence value and

그런 다음이 값은 수치 우선 값을 첨부하는 데 사용됩니다.
associativity direction to each grammar rule. *This is always determined

각 문법 규칙에 대한 연관 방향. *이것은 항상 결정됩니다
by looking at the precedence of the right-most terminal symbol.* For

가장 오른쪽에서 가장 오른쪽 터미널 기호의 우선 순위를 보면.*
example:

    expression : expression PLUS expression                 # level = 1, left
               | expression MINUS expression                # level = 1, left
               | expression TIMES expression                # level = 2, left
               | expression DIVIDE expression               # level = 2, left
               | LPAREN expression RPAREN                   # level = None (not specified)

| LPAREN 표현 RPAREN # level = 없음 (지정되지 않음)
               | NUMBER                                     # level = None (not specified)

| 번호 # 레벨 = 없음 (지정되지 않음)

When shift/reduce conflicts are encountered, the parser generator

교대/감소 충돌이 발생하면 파서 생성기
resolves the conflict by looking at the precedence rules and

우선 순위 규칙을보고 갈등을 해결하고
associativity specifiers.

연관성 지정자.

Yacc precedence and associativity of tokens:

토큰의 YACC 우선 순위와 연관성 :

1.  If the current token has higher precedence than the rule on the

1. 현재 토큰이의 규칙보다 우선 순위가 높은 경우
    stack, it is shifted.

스택, 그것은 이동됩니다.
2.  If the grammar rule on the stack has higher precedence, the rule is

2. 스택의 문법 규칙이 우선 순위가 높으면 규칙은
    reduced.

줄인.
3.  If the current token and the grammar rule have the same precedence,

3. 현재 토큰과 문법 규칙이 동일한 우선 순위를 갖는 경우
    the rule is reduced for left associativity, whereas the token is

왼쪽 연관성에 대한 규칙이 줄어든 반면 토큰은
    shifted for right associativity.

올바른 연관성을 위해 바뀌 었습니다.
4.  If nothing is known about the precedence, shift/reduce conflicts are

4. 우선 순위에 대해 알려진 것이 없다면, 교대/감소 충돌은 다음과 같습니다.
    resolved in favor of shifting (the default).

이동 (기본값)에 유리하게 해결되었습니다.

For example, if \"expression PLUS expression\" has been parsed and the

예를 들어, \ "expression plus expression \"가 구문 분석 된 경우
next token is \"TIMES\", the action is going to be a shift because

다음 토큰은 \ "Times \"이며, 행동은 변화가 될 것입니다.
\"TIMES\" has a higher precedence level than \"PLUS\". On the other

\ "Times \"는 \ "plus \"보다 우선 순위가 높습니다. 다른쪽에
hand, if \"expression TIMES expression\" has been parsed and the next

손, \ "expression times expression \"가 구문 분석 된 경우
token is \"PLUS\", the action is going to be reduce because \"PLUS\" has

토큰은 \ "plus \"이고, \ "plus \"가
a lower precedence than \"TIMES.\"

\ "Times. \"보다 우선 순위가 낮습니다.

When shift/reduce conflicts are resolved using the first three

교대/감소 충돌이 처음 세 개를 사용하여 해결 될 때
techniques (with the help of precedence rules), `yacc.py` will report no

기술 (우선 순위 규칙의 도움으로),`yacc.py`는 NO를보고합니다.
errors or conflicts in the grammar (although it will print some

문법의 오류 또는 충돌 (일부 인쇄하지만 일부는 인쇄하지만
information in the `parser.out` debugging file).

`parser.out '디버깅 파일의 정보).

One problem with the precedence specifier technique is that it is

우선 순위 지정 기술의 한 가지 문제는
sometimes necessary to change the precedence of an operator in certain

때로는 연산자의 우선 순위를 변경하는 데 필요합니다.
contexts. For example, consider a unary-minus operator in \"3 + 4 \*

맥락. 예를 들어, \ "3 + 4 \*의 unery-minus 연산자를 고려하십시오.
-5\". Mathematically, the unary minus is normally given a very high

-5 \ ". 수학적으로, 외형 마이너스는 일반적으로 매우 높습니다.
precedence\--being evaluated before the multiply. However, in our

우선 순위 \-곱하기 전에 평가됩니다. 그러나 우리에게
precedence specifier, MINUS has a lower precedence than TIMES. To deal

우선 순위 지정자, 마이너스는 시간보다 우선 순위가 낮습니다. 다루는
with this, precedence rules can be given for so-called \"fictitious

이를 통해 소위 \ "Fictitious에 대한 선행 규칙이 제공 될 수 있습니다.
tokens\" like this:

    precedence = (
        ('left', 'PLUS', 'MINUS'),
        ('left', 'TIMES', 'DIVIDE'),
        ('right', 'UMINUS'),            # Unary minus operator

( '오른쪽', 'Uminus'), # 단지 마이너스 운영자
    )

Now, in the grammar file, we can write our unary minus rule like this:

이제 Grammar 파일에서 우리는 다음과 같은 외형 마이너스 규칙을 쓸 수 있습니다.

    def p_expr_uminus(p):
        'expression : MINUS expression %prec UMINUS'
        p[0] = -p[2]

In this case, `%prec UMINUS` overrides the default rule

이 경우`%prec uminus`는 기본 규칙을 무시합니다.
precedence\--setting it to that of UMINUS in the precedence specifier.

우선 순위 \-우선 순위 지정자에서 Uminus의 것들로 설정합니다.

At first, the use of UMINUS in this example may appear very confusing.

처음에는이 예에서 Uminus의 사용이 매우 혼란스러워 보일 수 있습니다.
UMINUS is not an input token or a grammar rule. Instead, you should

Uminus는 입력 토큰 또는 문법 규칙이 아닙니다. 대신, 당신은해야합니다
think of it as the name of a special marker in the precedence table.

그것을 선행 테이블에서 특수 마커의 이름으로 생각하십시오.
When you use the `%prec` qualifier, you\'re telling yacc that you want

`%prec` Qualifier를 사용하면 yacc에게 원하는 것을 말합니다.
the precedence of the expression to be the same as for this special

표현의 우선 순위는이 특별한 것과 동일합니다.
marker instead of the usual precedence.

일반적인 우선 순위 대신 마커.

It is also possible to specify non-associativity in the `precedence`

'우선 순위'에서 비 연관성을 지정하는 것도 가능합니다.
table. This would be used when you *don\'t* want operations to chain

테이블. 이것은 당신이 * don \ 't *를 체인 할 작업을 원할 때 사용됩니다.
together. For example, suppose you wanted to support comparison

함께. 예를 들어, 비교를 지원하고 싶다고 가정 해 봅시다
operators like `<` and `>` but you didn\'t want to allow combinations

`<`및`>`을 좋아하는 연산자는 조합을 허용하지 않았습니다.
like `a < b < c`. To do this, specify a rule like this:

`a <b <c`처럼. 이렇게하려면 다음과 같은 규칙을 지정하십시오.

    precedence = (
        ('nonassoc', 'LESSTHAN', 'GREATERTHAN'),  # Nonassociative operators
        ('left', 'PLUS', 'MINUS'),
        ('left', 'TIMES', 'DIVIDE'),
        ('right', 'UMINUS'),            # Unary minus operator

( '오른쪽', 'Uminus'), # 단지 마이너스 운영자
    )

If you do this, the occurrence of input text such as `a < b < c` will

이렇게하면`a <b <c`와 같은 입력 텍스트가 발생합니다.
result in a syntax error. However, simple expressions such as `a < b`

구문 오류가 발생합니다. 그러나`a <b`와 같은 간단한 표현
will still be fine.

여전히 괜찮을 것입니다.

Reduce/reduce conflicts are caused when there are multiple grammar rules

여러 문법 규칙이있을 때 충돌 감소/감소가 발생합니다.
that can be applied to a given set of symbols. This kind of conflict is

주어진 기호 세트에 적용 할 수 있습니다. 이런 종류의 갈등입니다
almost always bad and is always resolved by picking the rule that

거의 항상 나쁘고 항상 해결됩니다.
appears first in the grammar file. Reduce/reduce conflicts are almost

문법 파일에 먼저 나타납니다. 충돌 감소/감소는 거의입니다
always caused when different sets of grammar rules somehow generate the

다른 문법 규칙이 어떻게 든 생성 될 때 항상 발생합니다.
same set of symbols. For example:

동일한 기호 세트. 예를 들어:

    assignment :  ID EQUALS NUMBER

할당 : ID 번호와 동일합니다
               |  ID EQUALS expression

    expression : expression PLUS expression
               | expression MINUS expression
               | expression TIMES expression
               | expression DIVIDE expression
               | LPAREN expression RPAREN
               | NUMBER

In this case, a reduce/reduce conflict exists between these two rules:

이 경우이 두 규칙 사이에 감소/감소 충돌이 있습니다.

    assignment  : ID EQUALS NUMBER

할당 : ID 번호와 동일합니다
    expression  : NUMBER

For example, if you wrote \"a = 5\", the parser can\'t figure out if

예를 들어, \ "a = 5 \"를 썼다면 파서는
this is supposed to be reduced as `assignment : ID EQUALS NUMBER` or

이것은`할당 : Id와 같은 숫자 '또는
whether it\'s supposed to reduce the 5 as an expression and then reduce

5를 표현으로 줄이고 감소시켜야하는지 여부
the rule `assignment : ID EQUALS expression`.

규칙`할당 : id는 표현식과 같습니다.

It should be noted that reduce/reduce conflicts are notoriously

갈등 감소/감소는 악명 높다는 점에 주목해야합니다.
difficult to spot looking at the input grammar. When a reduce/reduce

입력 문법을 보는 것은 어렵습니다. 감소/감소시
conflict occurs, `yacc()` will try to help by printing a warning message

충돌이 발생합니다.`yacc ()`경고 메시지를 인쇄하여 도움을 드릴 것입니다.
such as this:

이와 같은 :

    WARNING: 1 reduce/reduce conflict

경고 : 1 충돌 감소/감소
    WARNING: reduce/reduce conflict in state 15 resolved using rule (assignment -> ID EQUALS NUMBER)

경고 : 규칙을 사용하여 해결 된 상태 15의 충돌 감소/감소 (할당 -> ID 평등 번호)
    WARNING: rejected rule (expression -> NUMBER)

경고 : 거부 규칙 (표현 -> 번호)

This message identifies the two rules that are in conflict. However, it

이 메시지는 충돌중인 두 규칙을 식별합니다. 그러나, 그것은
may not tell you how the parser arrived at such a state. To try and

파서가 어떻게 그러한 상태에 도착했는지 말하지 않을 수 있습니다. 시도하고
figure it out, you\'ll probably have to look at your grammar and the

알아 내십시오, 당신은 아마도 당신의 문법을보아야 할 것입니다.
contents of the `parser.out` debugging file with an appropriately high

적절한 높은`parser.out '디버깅 파일의 내용
level of caffeination.

카페인의 수준.

### The parser.out file

### parser.out 파일

Tracking down shift/reduce and reduce/reduce conflicts is one of the

다운 시프트 추적/감소 및 감소/감소/감소는 중 하나입니다.
finer pleasures of using an LR parsing algorithm. To assist in

LR 구문 분석 알고리즘 사용에 대한 더 미세한 즐거움. 도움을주기 위해
debugging, `yacc.py` can create a debugging file called \'parser.out\'.

디버깅,`yacc.py`는 \ 'parser.out \'라는 디버깅 파일을 만들 수 있습니다.
To create this file, use `yacc.yacc(debug=True)`. The contents of this

이 파일을 만들려면`yacc.yacc (debug = true)`을 사용하십시오. 이것의 내용
file look like the following:

파일은 다음과 같습니다.

    Unused terminals:

사용하지 않은 터미널 :


    Grammar

    Rule 1     expression -> expression PLUS expression
    Rule 2     expression -> expression MINUS expression
    Rule 3     expression -> expression TIMES expression
    Rule 4     expression -> expression DIVIDE expression
    Rule 5     expression -> NUMBER
    Rule 6     expression -> LPAREN expression RPAREN

    Terminals, with rules where they appear

터미널, 규칙이 나타나는 규칙

    TIMES                : 3

시간 : 3
    error                : 
    MINUS                : 2
    RPAREN               : 6
    LPAREN               : 6
    DIVIDE               : 4
    PLUS                 : 1
    NUMBER               : 5

    Nonterminals, with rules where they appear

비 터미널, 그들이 나타나는 규칙이 있습니다

    expression           : 1 1 2 2 3 3 4 4 6 0


    Parsing method: LALR

구문 분석 방법 : lalr


    state 0

        S' -> . expression
        expression -> . expression PLUS expression
        expression -> . expression MINUS expression
        expression -> . expression TIMES expression
        expression -> . expression DIVIDE expression
        expression -> . NUMBER
        expression -> . LPAREN expression RPAREN

        NUMBER          shift and go to state 3

숫자 이동 및 상태 3로 이동합니다
        LPAREN          shift and go to state 2

LPAREN 이동 및 상태 2로 이동합니다


    state 1

        S' -> expression .
        expression -> expression . PLUS expression
        expression -> expression . MINUS expression
        expression -> expression . TIMES expression
        expression -> expression . DIVIDE expression

        PLUS            shift and go to state 6

또한 State 6로 이동하여 6
        MINUS           shift and go to state 5

마이너스 이동 및 상태 5로 이동합니다
        TIMES           shift and go to state 4

시간이 이동하여 상태 4로 이동합니다
        DIVIDE          shift and go to state 7

시프트를 나누고 상태 7로 이동하십시오


    state 2

        expression -> LPAREN . expression RPAREN
        expression -> . expression PLUS expression
        expression -> . expression MINUS expression
        expression -> . expression TIMES expression
        expression -> . expression DIVIDE expression
        expression -> . NUMBER
        expression -> . LPAREN expression RPAREN

        NUMBER          shift and go to state 3

숫자 이동 및 상태 3로 이동합니다
        LPAREN          shift and go to state 2

LPAREN 이동 및 상태 2로 이동합니다


    state 3

        expression -> NUMBER .

        $               reduce using rule 5

$ 규칙 5를 사용하여 줄입니다
        PLUS            reduce using rule 5

또한 규칙 5를 사용하여 줄입니다
        MINUS           reduce using rule 5

규칙 5를 사용하여 마이너스 감소
        TIMES           reduce using rule 5

규칙 5를 사용하여 시간이 줄어 듭니다
        DIVIDE          reduce using rule 5

규칙 5를 사용하여 감소를 나눕니다
        RPAREN          reduce using rule 5

규칙 5를 사용하여 RPAREN 감소


    state 4

        expression -> expression TIMES . expression
        expression -> . expression PLUS expression
        expression -> . expression MINUS expression
        expression -> . expression TIMES expression
        expression -> . expression DIVIDE expression
        expression -> . NUMBER
        expression -> . LPAREN expression RPAREN

        NUMBER          shift and go to state 3

숫자 이동 및 상태 3로 이동합니다
        LPAREN          shift and go to state 2

LPAREN 이동 및 상태 2로 이동합니다


    state 5

        expression -> expression MINUS . expression
        expression -> . expression PLUS expression
        expression -> . expression MINUS expression
        expression -> . expression TIMES expression
        expression -> . expression DIVIDE expression
        expression -> . NUMBER
        expression -> . LPAREN expression RPAREN

        NUMBER          shift and go to state 3

숫자 이동 및 상태 3로 이동합니다
        LPAREN          shift and go to state 2

LPAREN 이동 및 상태 2로 이동합니다


    state 6

        expression -> expression PLUS . expression
        expression -> . expression PLUS expression
        expression -> . expression MINUS expression
        expression -> . expression TIMES expression
        expression -> . expression DIVIDE expression
        expression -> . NUMBER
        expression -> . LPAREN expression RPAREN

        NUMBER          shift and go to state 3

숫자 이동 및 상태 3로 이동합니다
        LPAREN          shift and go to state 2

LPAREN 이동 및 상태 2로 이동합니다


    state 7

        expression -> expression DIVIDE . expression
        expression -> . expression PLUS expression
        expression -> . expression MINUS expression
        expression -> . expression TIMES expression
        expression -> . expression DIVIDE expression
        expression -> . NUMBER
        expression -> . LPAREN expression RPAREN

        NUMBER          shift and go to state 3

숫자 이동 및 상태 3로 이동합니다
        LPAREN          shift and go to state 2

LPAREN 이동 및 상태 2로 이동합니다


    state 8

        expression -> LPAREN expression . RPAREN
        expression -> expression . PLUS expression
        expression -> expression . MINUS expression
        expression -> expression . TIMES expression
        expression -> expression . DIVIDE expression

        RPAREN          shift and go to state 13

RPAREN 이동 및 상태 13로 이동합니다
        PLUS            shift and go to state 6

또한 State 6로 이동하여 6
        MINUS           shift and go to state 5

마이너스 이동 및 상태 5로 이동합니다
        TIMES           shift and go to state 4

시간이 이동하여 상태 4로 이동합니다
        DIVIDE          shift and go to state 7

시프트를 나누고 상태 7로 이동하십시오


    state 9

        expression -> expression TIMES expression .
        expression -> expression . PLUS expression
        expression -> expression . MINUS expression
        expression -> expression . TIMES expression
        expression -> expression . DIVIDE expression

        $               reduce using rule 3

$ 규칙 3을 사용하여 줄입니다
        PLUS            reduce using rule 3

또한 규칙 3을 사용하여 줄입니다
        MINUS           reduce using rule 3

규칙 3을 사용하여 마이너스 감소
        TIMES           reduce using rule 3

규칙 3을 사용하여 시간이 줄어 듭니다
        DIVIDE          reduce using rule 3

규칙 3을 사용하여 감소를 나눕니다
        RPAREN          reduce using rule 3

RPAREN 규칙 3을 사용하여 감소합니다

      ! PLUS            [ shift and go to state 6 ]

! 게다가 [교대 및 상태 6로 이동]
      ! MINUS           [ shift and go to state 5 ]

! 마이너스 [교대 및 상태 5로 이동]
      ! TIMES           [ shift and go to state 4 ]

! 시간 [전환 및 상태 4로 이동]
      ! DIVIDE          [ shift and go to state 7 ]

! 나누기 [교대 및 상태 7로 이동]

    state 10

        expression -> expression MINUS expression .
        expression -> expression . PLUS expression
        expression -> expression . MINUS expression
        expression -> expression . TIMES expression
        expression -> expression . DIVIDE expression

        $               reduce using rule 2

$ 규칙 2를 사용하여 줄입니다
        PLUS            reduce using rule 2

또한 규칙 2를 사용하여 줄입니다
        MINUS           reduce using rule 2

규칙 2를 사용하여 마이너스 감소
        RPAREN          reduce using rule 2

RPAREN은 규칙 2를 사용하여 감소합니다
        TIMES           shift and go to state 4

시간이 이동하여 상태 4로 이동합니다
        DIVIDE          shift and go to state 7

시프트를 나누고 상태 7로 이동하십시오

      ! TIMES           [ reduce using rule 2 ]

! 시간 [규칙 2를 사용하여 감소]
      ! DIVIDE          [ reduce using rule 2 ]

! 나누기 [규칙 2를 사용하여 감소]
      ! PLUS            [ shift and go to state 6 ]

! 게다가 [교대 및 상태 6로 이동]
      ! MINUS           [ shift and go to state 5 ]

! 마이너스 [교대 및 상태 5로 이동]

    state 11

        expression -> expression PLUS expression .
        expression -> expression . PLUS expression
        expression -> expression . MINUS expression
        expression -> expression . TIMES expression
        expression -> expression . DIVIDE expression

        $               reduce using rule 1

$ 규칙 1을 사용하여 줄입니다
        PLUS            reduce using rule 1

또한 규칙 1을 사용하여 줄입니다
        MINUS           reduce using rule 1

규칙 1을 사용하여 마이너스 감소
        RPAREN          reduce using rule 1

RPAREN은 규칙 1을 사용하여 감소합니다
        TIMES           shift and go to state 4

시간이 이동하여 상태 4로 이동합니다
        DIVIDE          shift and go to state 7

시프트를 나누고 상태 7로 이동하십시오

      ! TIMES           [ reduce using rule 1 ]

! 시간 [규칙 1을 사용하여 감소]
      ! DIVIDE          [ reduce using rule 1 ]

! 나누기 [규칙 1을 사용하여 감소]
      ! PLUS            [ shift and go to state 6 ]

! 게다가 [교대 및 상태 6로 이동]
      ! MINUS           [ shift and go to state 5 ]

! 마이너스 [교대 및 상태 5로 이동]

    state 12

        expression -> expression DIVIDE expression .
        expression -> expression . PLUS expression
        expression -> expression . MINUS expression
        expression -> expression . TIMES expression
        expression -> expression . DIVIDE expression

        $               reduce using rule 4

$ 규칙 4를 사용하여 줄입니다
        PLUS            reduce using rule 4

또한 규칙 4를 사용하여 줄입니다
        MINUS           reduce using rule 4

규칙 4를 사용하여 마이너스 감소
        TIMES           reduce using rule 4

규칙 4를 사용하여 시간이 줄어 듭니다
        DIVIDE          reduce using rule 4

규칙 4를 사용하여 감소를 나눕니다
        RPAREN          reduce using rule 4

규칙 4를 사용하여 RPAREN 감소

      ! PLUS            [ shift and go to state 6 ]

! 게다가 [교대 및 상태 6로 이동]
      ! MINUS           [ shift and go to state 5 ]

! 마이너스 [교대 및 상태 5로 이동]
      ! TIMES           [ shift and go to state 4 ]

! 시간 [전환 및 상태 4로 이동]
      ! DIVIDE          [ shift and go to state 7 ]

! 나누기 [교대 및 상태 7로 이동]

    state 13

        expression -> LPAREN expression RPAREN .

        $               reduce using rule 6

$ 규칙 6을 사용하여 줄입니다
        PLUS            reduce using rule 6

또한 규칙 6을 사용하여 줄입니다
        MINUS           reduce using rule 6

규칙 6을 사용하여 마이너스 감소
        TIMES           reduce using rule 6

규칙 6을 사용하여 시간이 줄어 듭니다
        DIVIDE          reduce using rule 6

규칙 6을 사용하여 감소를 나눕니다
        RPAREN          reduce using rule 6

규칙 6을 사용하여 RPAREN 감소

The different states that appear in this file are a representation of

이 파일에 나타나는 다른 상태는
every possible sequence of valid input tokens allowed by the grammar.

문법에 의해 허용되는 유효한 입력 토큰의 모든 가능한 시퀀스.
When receiving input tokens, the parser is building up a stack and

입력 토큰을받을 때 파서는 스택을 구축하고 있습니다.
looking for matching rules. Each state keeps track of the grammar rules

일치하는 규칙을 찾고 있습니다. 각주는 문법 규칙을 추적합니다
that might be in the process of being matched at that point. Within each

그것은 그 시점에서 일치하는 과정에있을 수 있습니다. 각각 내에서
rule, the ``.`` character indicates the current location of the parse

규칙,```.`` 캐릭터는 구문 분석의 현재 위치를 나타냅니다.
within that rule. In addition, the actions for each valid input token

그 규칙 내에서. 또한 각 유효한 입력 토큰에 대한 조치
are listed. When a shift/reduce or reduce/reduce conflict arises, rules

나열되어 있습니다. 교대/감소 또는 감소/감소/감소가 발생하면 규칙
*not* selected are prefixed with an ``!``. For example:

* 선택되지 않은* 선택은``!````와 접두사됩니다. 예를 들어:

    ! TIMES           [ reduce using rule 2 ]

! 시간 [규칙 2를 사용하여 감소]
    ! DIVIDE          [ reduce using rule 2 ]

! 나누기 [규칙 2를 사용하여 감소]
    ! PLUS            [ shift and go to state 6 ]

! 게다가 [교대 및 상태 6로 이동]
    ! MINUS           [ shift and go to state 5 ]

! 마이너스 [교대 및 상태 5로 이동]

By looking at these rules (and with a little practice), you can usually

이 규칙을 살펴보면 (그리고 약간의 연습으로)
track down the source of most parsing conflicts. It should also be

대부분의 구문 분석 충돌의 출처를 추적하십시오. 또한해야합니다
stressed that not all shift-reduce conflicts are bad. However, the only

모든 시프트 레디스 충돌이 나쁘지는 않다고 강조했습니다. 그러나 유일한 것
way to be sure that they are resolved correctly is to look at

그들이 올바르게 해결되었는지 확인하는 방법은
``parser.out`` file generated by ``yacc.py`` by default, can be disabled by passing ``False`` to debug::

``parser.out ''``yacc.py ''에 의해 생성 된 파일은 기본적으로``false````````는 디버그에 전달하여 비활성화 할 수 있습니다 ::

	yacc.yacc(debug=False)

### Syntax Error Handling

If you are creating a parser for production use, the handling of syntax

생산 사용을위한 파서를 만드는 경우 구문 처리
errors is important. As a general rule, you don\'t want a parser to

오류가 중요합니다. 일반적으로, 당신은 파서를 원하지 않습니다.
throw up its hands and stop at the first sign of trouble. Instead, you

손을 던지고 문제의 첫 징후를 멈추십시오. 대신, 당신
want it to report the error, recover if possible, and continue parsing

오류를보고하고 가능하면 복구하고 계속 구문 분석하기를 원합니다.
so that all of the errors in the input get reported to the user at once.

입력의 모든 오류가 한 번에 사용자에게보고되도록합니다.
This is the standard behavior found in compilers for languages such as

이것은 다음과 같은 언어의 컴파일러에서 발견되는 표준 동작입니다.
C, C++, and Java.

C, C ++ 및 Java.

In PLY, when a syntax error occurs during parsing, the error is

Ply에서 구문 분석 중에 구문 오류가 발생하면 오류는 다음과 같습니다.
immediately detected (i.e., the parser does not read any more tokens

즉시 감지 된 (즉, 파서는 더 이상 토큰을 읽지 않습니다.
beyond the source of the error). However, at this point, the parser

오류의 출처를 넘어서). 그러나이 시점에서 파서
enters a recovery mode that can be used to try and continue further

더 시도하고 계속 시도 할 수있는 복구 모드로 들어갑니다.
parsing. As a general rule, error recovery in LR parsers is a delicate

구문 분석. 일반적으로 LR 파서의 오류 복구는 섬세합니다.
topic that involves ancient rituals and black-magic. The recovery

고대 의식과 검은 마법과 관련된 주제. 회복
mechanism provided by `yacc.py` is comparable to Unix yacc so you may

`yacc.py`가 제공하는 메커니즘은 UNIX YACC와 비슷하므로
want consult a book like O\'Reilly\'s \"Lex and Yacc\" for some of the

일부의 경우 O \ 'Reilly \'S \ "Lex 및 Yacc \"와 같은 책을 참조하십시오.
finer details.

When a syntax error occurs, `yacc.py` performs the following steps:

구문 오류가 발생하면`yacc.py`는 다음 단계를 수행합니다.

1.  On the first occurrence of an error, the user-defined `p_error()`

1. 오류의 첫 번째 발생에서 사용자 정의`p_error ()`
    function is called with the offending token as an argument. However,

기능은 불쾌한 토큰으로 인수로 호출됩니다. 하지만,
    if the syntax error is due to reaching the end-of-file, `p_error()`

구문 오류가 파일 끝에 도달하기 때문에`p_error ()`
    is called with an argument of `None`. Afterwards, the parser enters

`none '이라는 주장과 함께 호출됩니다. 그 후 파서가 들어갑니다
    an \"error-recovery\" mode in which it will not make future calls to

\ "error-recovery \"모드는 향후 전화를 걸지 않을 것입니다.
    `p_error()` until it has successfully shifted at least 3 tokens onto

`p_error ()`는 3 개 이상의 토큰을 성공적으로 이동할 때까지
    the parsing stack.

구문 분석 스택.
2.  If no recovery action is taken in `p_error()`, the offending

2.`p_error ()`에서 복구 조치가 취해지지 않으면 불쾌감
    lookahead token is replaced with a special `error` token.

LookaheAd 토큰은 특별한 '오류'토큰으로 대체됩니다.
3.  If the offending lookahead token is already set to `error`, the top

3. 불쾌한 룩보드 토큰이 이미 'error'로 설정된 경우 상단
    item of the parsing stack is deleted.

구문 분석 스택의 항목이 삭제됩니다.
4.  If the entire parsing stack is unwound, the parser enters a restart

4. 전체 구문 분석 스택이 풀리면 파서가 다시 시작됩니다.
    state and attempts to start parsing from its initial state.

상태 및 초기 상태에서 구문 분석을 시작하려는 시도.
5.  If a grammar rule accepts `error` as a token, it will be shifted

5. 문법 규칙이 '오류'를 토큰으로 받아들이면 이동됩니다.
    onto the parsing stack.

구문 분석 스택에.
6.  If the top item of the parsing stack is `error`, lookahead tokens

6. 구문 분석 스택의 상단 항목이`error '인 경우 LookaheAd Tokens
    will be discarded until the parser can successfully shift a new

파서가 새로운 것을 성공적으로 바꿀 수있을 때까지 버릴 것입니다.
    symbol or reduce a rule involving `error`.

'error'와 관련된 규칙을 기호하거나 줄입니다.

#### Recovery and resynchronization with error rules

#### 오류 규칙을 통한 복구 및 재 동기화

The most well-behaved approach for handling syntax errors is to write

구문 오류를 처리하기위한 가장 잘 행동하는 접근 방식은 작성하는 것입니다.
grammar rules that include the `error` token. For example, suppose your

'오류'토큰을 포함하는 문법 규칙. 예를 들어, 당신의 말을 가정하십시오
language had a grammar rule for a print statement like this:

언어는 다음과 같은 인쇄문에 대한 문법 규칙을 가졌습니다.

    def p_statement_print(p):
         'statement : PRINT expr SEMI'
         ...

To account for the possibility of a bad expression, you might write an

나쁜 표현의 가능성을 설명하기 위해, 당신은
additional grammar rule like this:

다음과 같은 추가 문법 규칙 :

    def p_statement_print_error(p):
         'statement : PRINT error SEMI'
         print("Syntax error in print statement. Bad expression")

인쇄 ( "인쇄 문의 구문 오류. 나쁜 표현")

In this case, the `error` token will match any sequence of tokens that

이 경우 '오류'토큰은 모든 토큰 시퀀스와 일치합니다.
might appear up to the first semicolon that is encountered. Once the

발생한 첫 번째 세미콜론에 나타날 수 있습니다. 일단
semicolon is reached, the rule will be invoked and the `error` token

세미콜론에 도달하고 규칙이 호출되고 '오류'토큰이
will go away.

This type of recovery is sometimes known as parser resynchronization.

이 유형의 회복은 때때로 구문 분석 재 동기화라고도합니다.
The `error` token acts as a wildcard for any bad input text and the

'오류'토큰은 잘못된 입력 텍스트와
token immediately following `error` acts as a synchronization token.

`error '직후의 토큰은 동기화 토큰 역할을합니다.

It is important to note that the `error` token usually does not appear

'오류'토큰이 일반적으로 나타나지 않는다는 점에 유의해야합니다.
as the last token on the right in an error rule. For example:

오류 규칙에서 오른쪽의 마지막 토큰으로. 예를 들어:

    def p_statement_print_error(p):
        'statement : PRINT error'
        print("Syntax error in print statement. Bad expression")

인쇄 ( "인쇄 문의 구문 오류. 나쁜 표현")
This is because the first bad token encountered will cause the rule to

처음 만난 첫 번째 나쁜 토큰이 규칙을 유발하기 때문입니다.
be reduced\--which may make it difficult to recover if more bad tokens

줄어드는 \-더 나쁜 토큰이라면 회복하기가 어려울 수 있습니다.
immediately follow.

즉시 따릅니다.

#### Panic mode recovery

#### 공황 모드 복구

An alternative error recovery scheme is to enter a panic mode recovery

대체 오류 복구 체계는 공황 모드 복구에 들어가는 것입니다.
in which tokens are discarded to a point where the parser might be able

토큰이 파서가 할 수있는 지점까지 버려진
to recover in some sensible manner.

Panic mode recovery is implemented entirely in the `p_error()` function.

공황 모드 복구는 전적으로`p_error ()`함수에서 구현됩니다.
For example, this function starts discarding tokens until it reaches a

예를 들어,이 기능은 토큰이
closing \'}\'. Then, it restarts the parser in its initial state:

닫는 \ '} \'. 그런 다음 초기 상태에서 파서를 다시 시작합니다.

    def p_error(p):
        print("Whoa. You are seriously hosed.")

print ( "whoa. 당신은 심각하게 호스가 있습니다.")
        if not p:

P :
            print("End of File!")

print ( "파일 끝!")
            return

반품

        # Read ahead looking for a closing '}'

# 마감 '}'를 찾는 미리 읽기
        while True:

사실이지만 :
            tok = parser.token()             # Get the next token
            if not tok or tok.type == 'RBRACE': 

토크 나 토크가 아닌 경우 type == 'rbrace':
                break
        parser.restart()

This function discards the bad token and tells the parser that the error

이 기능은 나쁜 토큰을 버리고 구문자에게 오류가 발생한다고 말합니다.
was ok:

    def p_error(p):
        if p:
             print("Syntax error at token", p.type)
             # Just discard the token and tell the parser it's okay.

# 토큰을 버리고 파서에게 괜찮다고 말하십시오.
             parser.errok()
        else:
             print("Syntax error at EOF")

More information on these methods is as follows:

이 방법에 대한 자세한 내용은 다음과 같습니다.

`parser.errok()`

:   This resets the parser state so it doesn\'t think it\'s in

: 이것은 파서 상태를 재설정하므로 생각하지 않습니다.
    error-recovery mode. This will prevent an `error` token from being

오류 복구 모드. 이렇게하면 '오류'토큰이 존재하지 않습니다
    generated and will reset the internal error counters so that the

내부 오류 카운터를 생성하고 재설정하여
    next syntax error will call `p_error()` again.

다음 구문 오류는`p_error ()`을 다시 호출합니다.

`parser.token()`

:   This returns the next token on the input stream.

: 입력 스트림에서 다음 토큰을 반환합니다.

`parser.restart()`.

:   This discards the entire parsing stack and resets the parser to its

: 이것은 전체 구문 분석 스택을 버리고 파서를 그로 재설정합니다.
    initial state.

To supply the next lookahead token to the parser, `p_error()` can return

파서에 다음 룩 하이드 토큰을 공급하려면`p_error ()`can retoy
a token. This might be useful if trying to synchronize on special

토큰. 특별한 것과 동기화하려고하는 경우 유용 할 수 있습니다.
characters. For example:

캐릭터. 예를 들어:

    def p_error(p):
        # Read ahead looking for a terminating ";"

# 종료를 찾는 미리 읽기 ";"
        while True:

사실이지만 :
            tok = parser.token()             # Get the next token

tok = parser.token () # 다음 토큰을 얻습니다.
            if not tok or tok.type == 'SEMI': break
        parser.errok()

        # Return SEMI to the parser as the next lookahead token

# 다음 룩 하이드 토큰으로 파서에게 반 반환
        return tok  

Keep in mind in that the above error handling functions, `parser` is an

위의 오류 처리 함수는 'Parser'가
instance of the parser created by `yacc()`. You\'ll need to save this

`yacc ()`에 의해 생성 된 파서의 인스턴스. 당신은 이것을 저장해야합니다
instance someplace in your code so that you can refer to it during error

오류 중에 참조 할 수 있도록 코드의 인스턴스 인스턴스
handling.

#### Signalling an error from a production

#### 생산의 오류 신호

If necessary, a production rule can manually force the parser to enter

필요한 경우 생산 규칙이 수동으로 파서를 입력 할 수 있습니다.
error recovery. This is done by raising the `SyntaxError` exception like

오류 복구. 이것은`syntaxError '예외와 같은
this:

이것:

    def p_production(p):
        'production : some production ...'
        raise SyntaxError

The effect of raising `SyntaxError` is the same as if the last symbol

`syntaxerror`를 올리는 효과는 마지막 기호와 동일합니다.
shifted onto the parsing stack was actually a syntax error. Thus, when

구문 분석 스택으로 바뀌는 것은 실제로 구문 오류였습니다. 따라서 언제
you do this, the last symbol shifted is popped off of the parsing stack

이렇게하면 마지막으로 이동 한 기호가 구문 분석 스택에서 튀어 나옵니다.
and the current lookahead token is set to an `error` token. The parser

그리고 현재의 룩보드 토큰은 '오류'토큰으로 설정됩니다. 파서
then enters error-recovery mode where it tries to reduce rules that can

그런 다음 오류 복구 모드로 들어가서 규칙을 줄이려는 규칙을 줄입니다.
accept `error` tokens. The steps that follow from this point are exactly

'오류'토큰을 수락하십시오. 이 시점에서 다음 단계는 정확히 있습니다
the same as if a syntax error were detected and `p_error()` were called.

구문 오류가 감지되고`p_error ()`가 호출되는 것과 동일합니다.

One important aspect of manually setting an error is that the

수동으로 오류를 설정하는 데있어 중요한 측면 중 하나는
`p_error()` function will NOT be called in this case. If you need to

이 경우`p_error ()`함수는 호출되지 않습니다. 필요한 경우
issue an error message, make sure you do it in the production that

오류 메시지를 발행하고 프로덕션에서 수행하십시오.
raises `SyntaxError`.

Note: This feature of PLY is meant to mimic the behavior of the YYERROR

참고 : Ply 의이 특징은 Yyerror의 동작을 모방하기위한 것입니다.
macro in yacc.

#### When Do Syntax Errors Get Reported?

In most cases, yacc will handle errors as soon as a bad input token is

대부분의 경우 YACC는 입력 토큰이 잘못 되 자마자 오류를 처리합니다.
detected on the input. However, be aware that yacc may choose to delay

입력에서 감지되었습니다. 그러나 YACC는 지연을 선택할 수 있습니다.
error handling until after it has reduced one or more grammar rules

error handling until after it has reduced one or more grammar rules
first. This behavior might be unexpected, but it\'s related to special

첫 번째. 이 행동은 예상치 못한 일 수 있지만 특별한 것과 관련이 있습니다.
states in the underlying parsing table known as \"defaulted states.\" A

\ "기본 상태로 알려진 기본 구문 분석 테이블의 상태. \"a
defaulted state is parsing condition where the same grammar rule will be

기본 상태는 동일한 문법 규칙이있는 구문 분석 조건입니다.
reduced regardless of what *valid* token comes next on the input. For

입력에서 다음에 어떤 * 유효한 * 토큰이 오는지에 관계없이 줄어 듭니다. 을 위한
such states, yacc chooses to go ahead and reduce the grammar rule

그러한 상태에서 YACC는 계속해서 문법 규칙을 줄이기로 결정합니다.
*without reading the next input token*. If the next token is bad, yacc

*다음 입력 토큰을 읽지 않고*. 다음 토큰이 나쁘면, yacc
will eventually get around to reading it and report a syntax error.

결국 그것을 읽고 구문 오류를보고합니다.
It\'s just a little unusual in that you might see some of your grammar

그것은 당신이 당신의 문법을 볼 수 있다는 점에서 조금 특이한 것입니다.
rules firing immediately prior to the syntax error.

구문 오류 직전에 규칙이 발생합니다.

Usually, the delayed error reporting with defaulted states is harmless

일반적으로 기본 상태에 대한 지연 오류보고는 무해합니다.
(and there are other reasons for wanting PLY to behave in this way).

(그리고 Ply가 이런 식으로 행동하기를 원하는 다른 이유가 있습니다).
However, if you need to turn this behavior off for some reason. You can

그러나 어떤 이유로이 동작을 끄야한다면. 당신은 할 수 있습니다
clear the defaulted states table like this:

다음과 같은 기본 상태 테이블을 지우십시오.

    parser = yacc.yacc()
    parser.defaulted_states = {}

Disabling defaulted states is not recommended if your grammar makes use

문법을 사용하는 경우 기본 상태를 비활성화하는 것이 권장되지 않습니다.
of embedded actions as described in Section 6.11.

섹션 6.11에 설명 된 내장 조치.

#### General comments on error handling

#### 오류 처리에 대한 일반 의견

For normal types of languages, error recovery with error rules and

일반 유형의 언어의 경우 오류 규칙을 통한 오류 복구 및
resynchronization characters is probably the most reliable technique.

재 동기화 문자는 아마도 가장 신뢰할 수있는 기술 일 것입니다.
This is because you can instrument the grammar to catch errors at

문법이 오류를 잡을 수 있기 때문입니다.
selected places where it is relatively easy to recover and continue

복구가 상대적으로 쉬운 선택된 장소
parsing. Panic mode recovery is really only useful in certain

구문 분석. 공황 모드 복구는 실제로 유용합니다
specialized applications where you might want to discard huge portions

거대한 부분을 폐기하려는 특수 응용 프로그램
of the input text to find a valid restart point.

유효한 재시작 지점을 찾기위한 입력 텍스트의

### Line Number and Position Tracking

### 줄 번호 및 위치 추적

Position tracking is often a tricky problem when writing compilers. By

위치 추적은 종종 컴파일러를 작성할 때 까다로운 문제입니다. 에 의해
default, PLY tracks the line number and position of all tokens. This

기본값, Ply는 모든 토큰의 줄 번호와 위치를 추적합니다. 이것
information is available using the following functions:

정보는 다음 기능을 사용하여 사용할 수 있습니다.

`p.lineno(num)`. Return the line number for symbol *num*

`P.Lineno (num)`. 기호 *num *의 줄 번호를 반환합니다.

`p.lexpos(num)`. Return the lexing position for symbol *num*

`p.lexpos (num)`. 기호 *num *에 대한 Lexing 위치를 반환합니다.

For example:

예를 들어:

    def p_expression(p):
        'expression : expression PLUS expression'
        line   = p.lineno(2)        # line number of the PLUS token

line = p.lineno (2) # 플러스 토큰의 줄 번호
        index  = p.lexpos(2)        # Position of the PLUS token

index = p.lexpos (2) # 플러스 토큰의 위치

As an optional feature, `yacc.py` can automatically track line numbers

선택적 기능으로`yacc.py`는 라인 번호를 자동으로 추적 할 수 있습니다.
and positions for all of the grammar symbols as well. However, this

모든 문법 기호에 대한 위치. 그러나 이것
extra tracking requires extra processing and can significantly slow down

추가 추적에는 추가 처리가 필요하며 크게 속도가 느려질 수 있습니다.
parsing. Therefore, it must be enabled by passing the `tracking=True`

구문 분석. 따라서`tracking = true`를 통과하여 활성화해야합니다.
option to `yacc.parse()`. For example:

`yacc.parse ()`에 대한 옵션. 예를 들어:

    yacc.parse(data,tracking=True)

Once enabled, the `lineno()` and `lexpos()` methods work for all grammar

일단 활성화되면`lineno ()`및`lexpos ()`메소드는 모든 문법에 대해 작동합니다.
symbols. In addition, two additional methods can be used:

기호. 또한 두 가지 추가 방법을 사용할 수 있습니다.

`p.linespan(num)`. Return a tuple (startline,endline) with the starting

`p.linespan (num)`. 시작과 함께 튜플 (startline, endline)을 반환하십시오.
and ending line number for symbol *num*.

`p.lexspan(num)`. Return a tuple (start,end) with the starting and

`p.lexspan (num)`. 시작과 함께 튜플 (시작, 끝)을 반환하고
ending positions for symbol *num*.

기호 *num *에 대한 결말 위치.

For example:

예를 들어:

    def p_expression(p):
        'expression : expression PLUS expression'
        p.lineno(1)        # Line number of the left expression

P.Lineno (1) # 왼쪽 표현식의 줄 번호
        p.lineno(2)        # line number of the PLUS operator

P.Lineno (2) # 플러스 연산자의 줄 번호
        p.lineno(3)        # line number of the right expression

p.Lineno (3) # 올바른 표현식의 줄 번호
        ...
        start,end = p.linespan(3)    # Start,end lines of the right expression

start, end = p.linespan (3) # 시작, 올바른 표현의 끝 줄
        starti,endi = p.lexspan(3)   # Start,end positions of right expression

starti, endi = p.lexspan (3) # 시작, 올바른 표현의 끝 위치

Note: The `lexspan()` function only returns the range of values up to

참고 :`lexspan ()`함수는 값 범위 만 최대로 반환합니다.
the start of the last grammar symbol.

마지막 문법 기호의 시작.

Although it may be convenient for PLY to track position information on

Ply가 위치 정보를 추적하는 것이 편리 할 수 있지만
all grammar symbols, this is often unnecessary. For example, if you are

모든 문법 기호, 이것은 종종 불필요합니다. 예를 들어, 당신이 있다면
merely using line number information in an error message, you can often

오류 메시지에서 줄 번호 정보를 사용하면 종종
just key off of a specific token in the grammar rule. For example:

문법 규칙에서 특정 토큰을 키우십시오. 예를 들어:

    def p_bad_func(p):
        'funccall : fname LPAREN error RPAREN'
        # Line number reported from LPAREN token

# lparen 토큰에서보고 된 줄 번호
        print("Bad function call at line", p.lineno(2))

print ( "라인에서 불량 함수 호출", p.lineno (2))

Similarly, you may get better parsing performance if you only

마찬가지로, 당신은 당신이 만 더 나은 구문 분석 성능을 얻을 수 있습니다.
selectively propagate line number information where it\'s needed using

사용이 필요한 곳에서 줄 번호 정보를 선택적으로 전파합니다.
the `p.set_lineno()` method. For example:

`p.set_lineno ()`메소드. 예를 들어:

    def p_fname(p):
        'fname : ID'

'fname : id'
        p[0] = p[1]
        p.set_lineno(0,p.lineno(1))

PLY doesn\'t retain line number information from rules that have already

ply는 이미 가지고있는 규칙에서 줄 번호 정보를 유지하지 않습니다.
been parsed. If you are building an abstract syntax tree and need to

구문 분석되었습니다. 추상 구문 트리를 만들고있는 경우
have line numbers, you should make sure that the line numbers appear in

줄 번호가 있으면 줄 번호가
the tree itself.

나무 자체.

### AST Construction

### AST 구성

`yacc.py` provides no special functions for constructing an abstract

`yacc.py`는 초록을 구성하는 특별한 기능을 제공하지 않습니다.
syntax tree. However, such construction is easy enough to do on your

구문 트리. 그러나 그러한 건축은 당신의
own.

소유하다.

A minimal way to construct a tree is to create and propagate a tuple or

나무를 구성하는 최소한의 방법은 튜플을 만들고 전파하는 것입니다.
list in each grammar rule function. There are many possible ways to do

각 문법 규칙 기능에 나열하십시오. 할 수있는 방법에는 여러 가지가 있습니다
this, but one example would be something like this:

이것은하지만 한 가지 예는 다음과 같습니다.

    def p_expression_binop(p):
        '''expression : expression PLUS expression
                      | expression MINUS expression
                      | expression TIMES expression
                      | expression DIVIDE expression'''

        p[0] = ('binary-expression',p[2],p[1],p[3])

p [0] = ( '이진 발현', p [2], p [1], p [3])

    def p_expression_group(p):
        'expression : LPAREN expression RPAREN'
        p[0] = ('group-expression',p[2])

    def p_expression_number(p):

def p_expression_number (p) :
        'expression : NUMBER'
        p[0] = ('number-expression',p[1])

p [0] = ( '번호 표현', p [1])

Another approach is to create a set of data structure for different

또 다른 접근법은 다른 것을위한 데이터 구조 세트를 만드는 것입니다.
kinds of abstract syntax tree nodes and assign nodes to `p[0]` in each

추상 구문 트리 노드의 종류 및 각각에`p [0]`에 노드를 할당합니다.
rule. For example:

    class Expr: pass

    class BinOp(Expr):

클래스 Binop (expr) :
        def __init__(self,left,op,right):

        def __init__(self,left,op,right):
            self.left = left
            self.right = right

self.right = 맞습니다
            self.op = op

    class Number(Expr):

클래스 번호 (expr) :
        def __init__(self,value):
            self.value = value

    def p_expression_binop(p):

def p_expression_binop (p) :
        '''expression : expression PLUS expression
                      | expression MINUS expression
                      | expression TIMES expression
                      | expression DIVIDE expression'''

        p[0] = BinOp(p[1],p[2],p[3])

    def p_expression_group(p):
        'expression : LPAREN expression RPAREN'
        p[0] = p[2]

    def p_expression_number(p):

def p_expression_number (p) :
        'expression : NUMBER'
        p[0] = Number(p[1])

The advantage to this approach is that it may make it easier to attach

이 접근법의 장점은 부착하기 쉽게 만들 수 있다는 것입니다.
more complicated semantics, type checking, code generation, and other

더 복잡한 의미, 유형 확인, 코드 생성 및 기타
features to the node classes.

노드 클래스의 기능.

To simplify tree traversal, it may make sense to pick a very generic

트리 트래버스를 단순화하려면 매우 일반적인 것을 선택하는 것이 합리적 일 수 있습니다.
tree structure for your parse tree nodes. For example:

    class Node:
        def __init__(self,type,children=None,leaf=None):

def __init __ (자기, 유형, children = none, leaf = none) :
             self.type = type

self.type = 유형
             if children:
                  self.children = children
             else:
                  self.children = [ ]
             self.leaf = leaf

    def p_expression_binop(p):
        '''expression : expression PLUS expression
                      | expression MINUS expression
                      | expression TIMES expression
                      | expression DIVIDE expression'''

        p[0] = Node("binop", [p[1],p[3]], p[2])

### Embedded Actions

### 내장 된 행동

The parsing technique used by yacc only allows actions to be executed at

YACC가 사용하는 구문 분석 기술은 액션을 실행할 수 있습니다.
the end of a rule. For example, suppose you have a rule like this:

규칙의 끝. 예를 들어, 다음과 같은 규칙이 있다고 가정합니다.

    def p_foo(p):

def p_foo (p) :
        "foo : A B C D"

"Foo : A B C D"
        print("Parsed a foo", p[1],p[2],p[3],p[4])

print ( "parsed a foo", p [1], p [2], p [3], p [4])

In this case, the supplied action code only executes after all of the

이 경우 제공된 조치 코드는 모든 후에 만 실행됩니다.
symbols `A`, `B`, `C`, and `D` have been parsed. Sometimes, however, it

기호`a`,`b`,`c` 및`d '가 구문 분석되었습니다. 그러나 때때로, 그것은
is useful to execute small code fragments during intermediate stages of

중간 단계에서 작은 코드 조각을 실행하는 데 유용합니다.
parsing. For example, suppose you wanted to perform some action

구문 분석. 예를 들어, 어떤 행동을 수행하고 싶다고 가정 해
immediately after `A` has been parsed. To do this, write an empty rule

`a`가 구문 분석 직후에. 이렇게하려면 빈 규칙을 작성하십시오
like this:

    def p_foo(p):

def p_foo (p) :
        "foo : A seen_A B C D"

"Foo : Seen_A B C D"
        print("Parsed a foo", p[1],p[3],p[4],p[5])

print ( "parsed a foo", p [1], p [3], p [4], p [5])
        print("seen_A returned", p[2])

print ( "seen_a returned", p [2])

    def p_seen_A(p):
        "seen_A :"
        print("Saw an A = ", p[-1])   # Access grammar symbol to left

print ( "a = a =", p [-1]) # 왼쪽에 문법 기호에 액세스
        p[0] = some_value            # Assign value to seen_A

In this example, the empty `seen_A` rule executes immediately after `A`

이 예에서 빈`seen_a` 규칙은`a` 직후에 실행됩니다.
is shifted onto the parsing stack. Within this rule, `p[-1]` refers to

구문 분석 스택으로 이동합니다. 이 규칙 내에서`p [-1]``는 다음을 말합니다.
the symbol on the stack that appears immediately to the left of the

즉시 왼쪽에 나타나는 스택의 기호
`seen_A` symbol. In this case, it would be the value of `A` in the `foo`

`seen_a '기호. 이 경우`foo`에서`a`의 값이 될 것입니다.
rule immediately above. Like other rules, a value can be returned from

바로 위의 규칙. 다른 규칙과 마찬가지로 값은
an embedded action by assigning it to `p[0]`

`p [0]`에 할당함으로써 임베디드 조치

The use of embedded actions can sometimes introduce extra shift/reduce

임베디드 작업을 사용하면 때때로 추가 교대/감소를 도출 할 수 있습니다.
conflicts. For example, this grammar has no conflicts:

갈등. 예를 들어,이 문법은 충돌이 없습니다.

    def p_foo(p):

def p_foo (p) :
        """foo : abcd
               | abcx"""

    def p_abcd(p):
        "abcd : A B C D"

"ABCD : A B C D"

    def p_abcx(p):
        "abcx : A B C X"

However, if you insert an embedded action into one of the rules like

그러나 다음과 같은 규칙 중 하나에 포함 된 조치를 삽입하는 경우
this:

이것:

    def p_foo(p):

def p_foo (p) :
        """foo : abcd
               | abcx"""

    def p_abcd(p):
        "abcd : A B C D"

"ABCD : A B C D"

    def p_abcx(p):
        "abcx : A B seen_AB C X"

"ABCX : A B Seen_AB C X"

    def p_seen_AB(p):
        "seen_AB :"

an extra shift-reduce conflict will be introduced. This conflict is

여분의 교대-감 빨대 충돌이 도입 될 것입니다. 이 갈등은입니다
caused by the fact that the same symbol `C` appears next in both the

동일한 기호`c`가 다음에 다음에 나타나는 사실로 인해 발생합니다.
`abcd` and `abcx` rules. The parser can either shift the symbol (`abcd`

`abcd`와`abcx '규칙. 파서는 기호를 이동할 수 있습니다 (`abcd`
rule) or reduce the empty rule `seen_AB` (`abcx` rule).

규칙) 또는 빈 규칙`seen_ab` (`ABCX` 규칙)을 줄입니다.

A common use of embedded rules is to control other aspects of parsing

임베디드 규칙의 일반적인 사용은 구문 분석의 다른 측면을 제어하는 것입니다.
such as scoping of local variables. For example, if you were parsing C

로컬 변수의 범위와 같은. 예를 들어, 구문 분석중인 경우 c
code, you might write code like this:

코드, 다음과 같은 코드를 작성할 수 있습니다.

    def p_statements_block(p):
        "statements: LBRACE new_scope statements RBRACE"""
        # Action code

        # Action code
        ...
        pop_scope()        # Return to previous scope

POP_SCOPE () # 이전 범위로 돌아갑니다

    def p_new_scope(p):

def p_new_scope (p) :        "new_scope :"
        # Create a new scope for local variables

# 로컬 변수에 대한 새로운 범위를 만듭니다
        s = new_scope()

s = new_scope ()
        push_scope(s)

푸시 _scope (들)
        ...

In this case, the embedded action `new_scope` executes immediately after

이 경우, 내장 된 조치`new_scope`는 즉시 실행됩니다.
a `LBRACE` (`{`) symbol is parsed. This might adjust internal symbol

`lbrace` (`{`) 기호가 구문 분석됩니다. 이것은 내부 기호를 조정할 수 있습니다
tables and other aspects of the parser. Upon completion of the rule

파서의 테이블 및 기타 측면. 규칙이 완료되면
`statements_block`, code might undo the operations performed in the

`statements_block`, 코드는
embedded action (e.g., `pop_scope()`).

임베디드 조치 (예 :`pop_scope ()`).

### Miscellaneous Yacc Notes

### Miscellaneous Yacc Notes

1.  By default, `yacc.py` relies on `lex.py` for tokenizing. However, an

1. 기본적으로`yacc.py`는 토큰 화를 위해`lex.py`에 의존합니다. 그러나, an
    alternative tokenizer can be supplied as follows:

대체 토큰 화기는 다음과 같이 공급할 수 있습니다.

        parser = yacc.parse(lexer=x)

    in this case, `x` must be a Lexer object that minimally has a

이 경우`X`는 최소한의 렉서 객체 여야합니다.
    `x.token()` method for retrieving the next token. If an input string

`x.token ()`다음 토큰 검색 방법. 입력 문자열 인 경우
    is given to `yacc.parse()`, the lexer must also have an `x.input()`

`yacc.parse ()`에 주어지면 Lexer에는`x.input ()`가 있어야합니다.
    method.

2.  To print copious amounts of debugging during parsing, use:

2. 구문 분석 중에 많은 양의 디버깅을 인쇄하려면 사용하십시오.

        parser.parse(input_text, debug=True)     

3.  Since LR parsing is driven by tables, the performance of the parser

3. LR 파싱은 테이블에 의해 구동되므로 구문 분석기의 성능
    is largely independent of the size of the grammar. The biggest

문법의 크기와 크게 독립적입니다. 가장 큰
    bottlenecks will be the lexer and the complexity of the code in your

병목 현상은 Lexer와 Code의 복잡성이됩니다.
    grammar rules.

4.  `yacc()` also allows parsers to be defined as classes and as

4.`yacc ()`또한 파서를 클래스로 정의하고
    closures (see the section on alternative specification of lexers).

클로저 (Lexers의 대체 사양에 관한 섹션 참조).
    However, be aware that only one parser may be defined in a single

그러나 하나의 파서 만 단일로 정의 될 수 있습니다.
    module (source file). There are various error checks and validation

모듈 (소스 파일). 다양한 오류 확인 및 검증이 있습니다
    steps that may issue confusing error messages if you try to define

정의하려고하는 경우 혼란스러운 오류 메시지를 발행 할 수있는 단계
    multiple parsers in the same source file.

동일한 소스 파일의 여러 파서.

## Multiple Parsers and Lexers

## 다중 파서 및 렉서스

In advanced parsing applications, you may want to have multiple parsers

Advanced Parsing Applications에서는 여러 개의 구문 분석기를 원할 수 있습니다.
and lexers.

그리고 렉서스.

As a general rules this isn\'t a problem. However, to make it work, you

일반적인 규칙으로 이것은 문제가되지 않습니다. 그러나 그것을 작동시키기 위해, 당신은 당신입니다
need to carefully make sure everything gets hooked up correctly. First,

모든 것이 올바르게 연결되도록 조심스럽게 조심스럽게 연결해야합니다. 첫 번째,
make sure you save the objects returned by `lex()` and `yacc()`. For

`lex ()`및`yacc ()`가 반환 한 객체를 저장하십시오. 을 위한
example:

    lexer  = lex.lex()       # Return lexer object
    parser = yacc.yacc()     # Return parser object

parser = yacc.yacc () # return parser 객체

Next, when parsing, make sure you give the `parse()` function a

다음으로, 구문 분석 할 때`parse ()`function a를 제공하십시오.
reference to the lexer it should be using. For example:

Lexer에 대한 참조는 사용해야합니다. 예를 들어:

    parser.parse(text,lexer=lexer)

If you forget to do this, the parser will use the last lexer

이 작업을 잊어 버린 경우 파서는 마지막 Lexer를 사용합니다.
created\--which is not always what you want.

만들어진 \- 이것은 항상 당신이 원하는 것이 아닙니다.

Within lexer and parser rule functions, these objects are also

Lexer 및 Parser Rule 기능 내에서 이러한 개체는 또한
available. In the lexer, the \"lexer\" attribute of a token refers to

사용 가능. Lexer에서 토큰의 \ "Lexer \"속성은
the lexer object that triggered the rule. For example:

규칙을 유발 한 Lexer 객체. 예를 들어:

    def t_NUMBER(t):
       r'\d+'
       ...
       print(t.lexer)           ## Show lexer object

인쇄 (t.lexer) ## lexer 객체를 보여줍니다

In the parser, the \"lexer\" and \"parser\" attributes refer to the

파서에서 \ "lexer \"및 \ "parser \"속성을 참조하십시오.
lexer and parser objects respectively:

Lexer 및 Parser 객체 각각 :

    def p_expr_plus(p):
       'expr : expr PLUS expr'
       ...
       print(p.parser)          # Show parser object

print (p.parser) # show parser 객체
       print(p.lexer)           # Show lexer object

인쇄 (p.lexer) # Show Lexer Object

If necessary, arbitrary attributes can be attached to the lexer or

필요한 경우 임의 속성을 Lexer에 첨부하거나
parser object. For example, if you wanted to have different parsing

파서 대상. 예를 들어, 다른 구문 분석을 원한다면
modes, you could attach a mode attribute to the parser object and look

모드, 파서 객체에 모드 속성을 첨부하고 보입니다.
at it later.

나중에.

## Advanced Debugging

Debugging a compiler is typically not an easy task. PLY provides some

컴파일러를 디버깅하는 것은 일반적으로 쉬운 일이 아닙니다. Ply는 일부를 제공합니다
diagostic capabilities through the use of Python\'s `logging` module.

Python의 '로깅'모듈 사용을 통한 진단 기능.
The next two sections describe this:

다음 두 섹션에서는 다음을 설명합니다.

### Debugging the lex() and yacc() commands

### lex () 및 yacc () 명령 디버깅

Both the `lex()` and `yacc()` commands have a debugging mode that can be

`lex ()`및`yacc ()`명령 모두 디버깅 모드가 있습니다.
enabled using the `debug` flag. For example:

'디버그'플래그를 사용하여 활성화했습니다. 예를 들어:

    lex.lex(debug=True)
    yacc.yacc(debug=True)

Normally, the output produced by debugging is routed to either standard

일반적으로 디버깅으로 생성 된 출력은 표준으로 라우팅됩니다.
error or, in the case of `yacc()`, to a file `parser.out`. This output

오류 또는`yacc ()`의 경우 파일`parser.out '에. 이 출력
can be more carefully controlled by supplying a logging object. Here is

벌목 객체를 공급하여보다 신중하게 제어 할 수 있습니다. 여기에 있습니다
an example that adds information about where different debugging

다른 디버깅 위치에 대한 정보를 추가하는 예
messages are coming from:

메시지는 다음과 같습니다.

    # Set up a logging object

# 로깅 객체를 설정합니다
    import logging
    logging.basicConfig(
        level = logging.DEBUG,
        filename = "parselog.txt",
        filemode = "w",
        format = "%(filename)10s:%(lineno)4d:%(message)s"
    )
    log = logging.getLogger()

    lex.lex(debug=True,debuglog=log)
    yacc.yacc(debug=True,debuglog=log)

If you supply a custom logger, the amount of debugging information

사용자 정의 로거를 제공하는 경우 디버깅 정보의 양
produced can be controlled by setting the logging level. Typically,

로깅 레벨을 설정하여 생성 될 수 있습니다. 일반적으로,
debugging messages are either issued at the `DEBUG`, `INFO`, or

디버깅 메시지는`debug`,`info '또는 또는
`WARNING` levels.

PLY\'s error messages and warnings are also produced using the logging

Ply의 오류 메시지 및 경고도 로깅을 사용하여 생성됩니다.
interface. This can be controlled by passing a logging object using the

상호 작용. 이것은
`errorlog` parameter:

    lex.lex(errorlog=log)
    yacc.yacc(errorlog=log)

If you want to completely silence warnings, you can either pass in a

경고를 완전히 침묵 시키려면
logging object with an appropriate filter level or use the `NullLogger`

적절한 필터 레벨이있는 로깅 객체 또는 'NullLogger'를 사용하십시오.
object defined in either `lex` or `yacc`. For example:

`lex` 또는`yacc`에 정의 된 객체. 예를 들어:

    yacc.yacc(errorlog=yacc.NullLogger())

### Run-time Debugging

To enable run-time debugging of a parser, use the `debug` option to

파서의 런타임 디버깅을 활성화하려면 '디버그'옵션을 사용하십시오.
parse. This option can either be an integer (which turns debugging on or

구문 분석. 이 옵션은 정수가 될 수 있습니다 (디버깅을 켜거나
off) or an instance of a logger object. For example:

OFF) 또는 로거 객체의 인스턴스. 예를 들어:

    log = logging.getLogger()
    parser.parse(input,debug=log)

If a logging object is passed, you can use its filtering level to

로깅 객체가 전달되면 필터링 레벨을 사용할 수 있습니다.
control how much output gets generated. The `INFO` level is used to

생성되는 출력의 양을 제어하십시오. '정보'레벨은 사용됩니다
produce information about rule reductions. The `DEBUG` level will show

규칙 감소에 대한 정보를 생성합니다. '디버그'레벨이 표시됩니다
information about the parsing stack, token shifts, and other details.

구문 분석 스택, 토큰 교대 및 기타 세부 사항에 대한 정보.
The `ERROR` level shows information related to parsing errors.

'오류'레벨은 구문 분석 오류와 관련된 정보를 보여줍니다.

For very complicated problems, you should pass in a logging object that

매우 복잡한 문제의 경우 로깅 객체를 전달해야합니다.
redirects to a file where you can more easily inspect the output after

이후 출력을보다 쉽게 검사 할 수있는 파일로 리디렉션
execution.

## Using Python -OO Mode

## Python -OO 모드 사용

Because of PLY\'s reliance on docstrings, it is not compatible with

ply의 docstrings에 대한 의존으로 인해 호환되지 않습니다.
[-OO]{.title-ref} mode of the interpreter (which strips docstrings). If

[-OO] {. TITLE-Ref} 통역사의 모드 (DOCSTRINGS 스트립). 만약에
you want to support this, you\'ll need to write a decorator or some

당신은 이것을 지원하고 싶습니다. 당신은 데코레이터 또는 일부를 써야 할 것입니다.
other tool to attach docstrings to functions. For example::

Docstrings를 함수에 첨부하는 다른 도구. 예를 들어::

    def _(doc):
        def decorate(func):
            func.__doc__ = doc
            return func
        return decorate

    @_("assignment : expr PLUS expr")
    def p_assignment(p):
        ...

PLY does not provide such a decorator by default.

PLY does not provide such a decorator by default.

## Where to go from here?

## 여기서 어디로 가야합니까?

The `examples` directory of the PLY distribution contains several simple

Ply 배포의 '예제'디렉토리에는 몇 가지 간단한
examples. Please consult a compilers textbook for the theory and

예. 이론에 대한 컴파일러 교과서를 참조하십시오
underlying implementation details or LR parsing.
기본 구현 세부 사항 또는 LR 구문 분석.