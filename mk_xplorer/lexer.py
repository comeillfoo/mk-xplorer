#!/usr/bin/env python3
import ply.lex as lex


tokens = (
    'INCLUDE',
    'DEFINE',
    'ENDEF',
    'COLON',
    'EQUAL',
    'PLUS',
    'QMARK',
    'XMARK',
    'DOLLAR',
    'LPAREN',
    'RPAREN',
    'WORD',
    'NEWLINE',
    'ESCNLINE',
    'TAB', # may be redefined at runtime by .RECIPEPREFIX
    'SPACE',
)

t_INCLUDE = r'include'
t_DEFINE = r'define'
t_ENDEF = r'endef'
t_COLON = r':'
t_EQUAL = r'='
t_PLUS = r'\+'
t_QMARK = r'\?'
t_XMARK = r'!'
t_DOLLAR = r'\$'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_WORD = r'\w+'
t_NEWLINE = r'\n'
t_ESCNLINE = r'\\\n'
t_TAB = r'\t'
t_SPACE = r'[ ]'

t_ignore = '\r\f\v'


def t_COMMENT(t):
    r'\#.*'
    pass
    # No return value. Token discarded

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

lexer = lex.lex()
