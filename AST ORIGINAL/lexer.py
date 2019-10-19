import ply.lex as lex

import re

keywords = (
            'boolean',
            'byte',
            'short',
            'int',
            'long',
            'char',
            'float',
            'double',
            'public',
            'private',
            'protected',
            'static',
            'abstract',
            'final',
            'native',
            'class',
            'main',
            'void',
            'if',
            'else',
            'while',
            'break',
            'return',
            'continue',
            'true',
            'false',
            'null',
            'String',
            'do'
            )
tokens = [
    'NAME',
    'NUM',
    'CHAR_LITERAL',
    'STRING_LITERAL',
    'UMINUS','ADD','MUL','DIV','SUB',

    'OR', 'AND',
    'EQ', 'NEQ', 'GTEQ', 'LTEQ','LESS','GREATER',
    'ASSIGN',
    'TIMES_ASSIGN', 'DIVIDE_ASSIGN', 'REMAINDER_ASSIGN',
    'PLUS_ASSIGN', 'MINUS_ASSIGN',

    'PLUSPLUS', 'MINUSMINUS',
] + [k.upper() for k in keywords]
literals = '()+-*/=?:,.^|&~!=[]{};<>@%'

t_NUM = r'\.?[0-9][0-9eE_lLdDa-fA-F.xXpP]*'
t_CHAR_LITERAL = r'\'([^\\\n]|(\\.))*?\''
t_STRING_LITERAL = r'\"([^\\\n]|(\\.))*?\"'

t_ignore_LINE_COMMENT = '//.*'

def t_BLOCK_COMMENT(t):
    r'/\*(.|\n)*?\*/'
    t.lexer.lineno +=  t.value.count('\n')

t_OR = r'\|\|'
t_AND = '&&'
t_DIV = r'\/'
t_EQ = '=='
t_NEQ = '!='
t_GTEQ = '>='
t_LTEQ = '<='
t_TIMES_ASSIGN = r'\*='
t_DIVIDE_ASSIGN = '/='
t_REMAINDER_ASSIGN = '%='
t_PLUS_ASSIGN = r'\+='
t_MINUS_ASSIGN = '-='
t_ASSIGN = r'='
t_SUB = r'\-'
t_UMINUS = r'\-'
t_PLUSPLUS = r'\+\+'
t_MINUSMINUS = r'\-\-'
t_ADD = r'\+'
t_MUL = r'\*'
t_LESS = r'<'
t_GREATER = r'>'
t_ignore = ' \t\f'

def t_NAME(t):
    '[A-Za-z_$][A-Za-z0-9_$]*'
    if t.value in keywords:
        t.type = t.value.upper()
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno +=  t.value.count("\n")

def t_error(t):
    #print("Illegal character '{}' ({}) in line {}".format(t.value[0], hex(ord(t.value[0])), t.lexer.lineno))
    t.lexer.skip(1)