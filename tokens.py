from enum import Enum, auto


class TokenType(Enum):
    LEFT_PAREN = auto() # (
    RIGHT_PAREN = auto() # )
    LEFT_BRACE = auto() # {
    RIGHT_BRACE = auto() # }
    LEFT_BRACKET = auto() # [
    RIGHT_BRACKET = auto() # ]
    SEMICOLON = auto() # ;

    COMMA = auto() # ,
    DOT = auto() # .
    PLUS = auto() # +
    MINUS = auto() # -
    STAR = auto() # *
    SLASH = auto() # /

    EQUAL = auto() # =
    EQUAL_EQUAL = auto() # ==
    EXCLAM = auto() # !
    EXCLAM_EQUAL = auto() # !=
    GREATER = auto() # >
    GREATER_EQUAL = auto() # >=
    LESS = auto() # <
    LESS_EQUAL = auto() # <=

    IDENTIFIER = auto() # Variable name, Function name, etc... ([a-zA-Z][a-zA-Z0-9]*)

    BOOLEAN = auto() # true, false
    INTEGER = auto() # Digit([0-9]+(.[0-9]*)?)
    SINGLE_STRING = auto() # 'string'
    DOUBLE_STRING = auto() # "string"
    BACKTICK_STRING = auto()

    EOF = auto() # End of file

    # Keywords
    IMPORT = "hugging"
    IF = 'if'
    ELSE = 'else'
    AND = 'and'
    OR = 'or'
    DEF = 'con'
    VAR = 'var'
    TRUE = 'true'
    FALSE = 'false'
    NULL = 'empty'
    FOR = 'for'
    WHILE = 'while'
    IN = 'in'
    GIVE = 'give'
    CLASS = 'certy'

    @classmethod
    def has_value(cls, value):
        return any(value == item.value for item in cls)
