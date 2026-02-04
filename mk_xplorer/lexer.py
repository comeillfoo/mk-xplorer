#!/usr/bin/env python3
import ply.lex as lex


reserved = {
    'include': 'INCLUDE',
    'define': 'DEFINE',
    'endef': 'ENDEF',
}


tokens = (
    'COLON',
    'EQUAL',
    'PLUS',
    'QMARK',
    'XMARK',
    'DOLLAR',
    'LPAREN',
    'RPAREN',
    'WORD',
    'NEWLINES',
    'ESCSEQ',
    'TABS', # may be redefined at runtime by .RECIPEPREFIX
    'SPACES',
) + tuple(reserved.values())


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
t_ESCSEQ = r'\\(u[A-Fa-f0-9]{4}|U[A-Fa-f0-9]{8}|.|\n)'

t_ignore = '\r\f\v'


def t_WORD(t):
    r'\w+'
    t.type = reserved.get(t.value, 'WORD')
    return t


def t_COMMENT(t):
    r'\#.*'
    pass
    # No return value. Token discarded


def t_NEWLINES(t):
    r'\n+'
    t.lexer.lineno += len(t.value)
    return t


def t_SPACES(t):
    r'[ ]+'
    t.value = len(t.value)
    return t


def t_TABS(t):
    r'\t+'
    t.value = len(t.value)
    return t


def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


lexer = lex.lex()
