import ply.lex as lex

import re


#THE FOLLOWING LINE HAS TO BE REMOVED
CONST_SPECIAL_CHARACTERS = u'\xf1\xe1\xe9\xed\xf3\xfa\xc1\xc9\xcd\xd3\xda\xd1'

## Token definition ##

tokens = [
          ''
          'AND',
          'ASSIGNMENT',
          'BINARY',
          'COMMA',
          'LINECOMMENT',
          'MULTILINECOMMENT',
          'RIGHTSQRBRACKET',
          'LEFTSQRBRACKET',
          'DIVISION',
          'NOTEQUAL',
          'CONCAT',
          'EQUAL',
          'NOT',
          'HEXADEC',
          'IDEN',
          'RIGHTBRACE',
          'LEFTBRACE',
          'GREATEREQUAL',
          'GREATER',
          'LESSEQUAL',
          'LESS',
          'SUBSTRACTION',
          'UMINUS',
          'MULTIPLICATION',
          'NUMBER',
          'CIENTIFIC',
          'DECIMAL',
          'OR',
          'RIGHTPARENT',
          'LEFTPARENT',
          'MODULO',
          'DOT',
          'SEMICOLON',
          'ADDITION'
          ]

## Store reserved words in dictionary ##

reserved = {
            'import': 'IMPORT', 
            'package': 'PACKAGE',
            'byte': 'BYTE',
            'short': 'SHORT',
            'int': 'INT',
            'long': 'LONG',
            'char': 'CHAR',
            'float': 'FLOAT',
            'double': 'DOUBLE',
            'public': 'PUBLIC',
            'private ': 'PRIVATE',
            'protected': 'PROTECTED',
            'static': 'STATIC',
            'abstract': 'ABSTRACT',
            'final': 'FINAL',
            'native': 'NATIVE',
            'class': 'CLASS',
            'main': 'MAIN',
            'void': 'VOID',
            'if': 'IF',
            'else': 'ELSE',
            'while': 'WHILE',
            'break': 'BREAK',
            'return': 'RETURN',
            'continue': 'CONTINUE'
}

## Merge tokens and reserved words ##

tokens += reserved.values()

##  Literal Token implementation ##

t_AND = r'(\&\&|AND)'
t_ASSIGNMENT = r'='
t_COMMA = r','
t_LEFTSQRBRACKET = r'\['
t_RIGHTSQRBRACKET = r'\]'
t_DIVISION = r'\/'
t_NOTEQUAL = r'!='
t_EQUAL = r'=='
t_NOT = r'!'
t_LEFTBRACE  = r'\{'
t_RIGHTBRACE = r'\}'
t_GREATEREQUAL = r'>='
t_GREATER = r'>'
t_LESSEQUAL = r'<='
t_LESS = r'<'
t_SUBSTRACTION = r'\-'
t_UMINUS = r'\-'
t_CONCAT = r'\+'
t_MULTIPLICATION = r'\*'
t_OR = r'(\|\|)|(OR)'
t_LEFTPARENT = r'\('
t_RIGHTPARENT = r'\)'
t_MODULO = r'%'
t_DOT = r'\.'
t_SEMICOLON = r';'
t_ADDITION = r'\+'

def t_DECIMAL(t):
    r'(-)?(\d+\.\d+)'
    return t

def t_NUMBER(t):
    r'(-)?(\d+)'
    try:
        t.value = int(t.value)
    except ValueError:
        print("ERROR CONVERSION NUMERO %d", t.value)
        t.value = 0
    return t

def t_IDEN(t):
    r'[_a-zA-Z_][a-zA-Z_0]*'
    t.value = accentReplace(t.value)
    t.type = reserved.get(t.value,'IDEN')
    if len(t.value)>20:
        t.value = t.value[:20]
    return t

def t_STRING(t):
    r'\"( ([ -~]|(\\\"))+ )\"'
    return t

def t_ignore_LINECOMMENT(t):
    r'//(.)*(\n)?'

def t_ignore_MULTILINECOMMENT(t):
    r'(/\*)(.|\n|\r)*(\*\/)'

t_ignore = " \t"

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")

def t_error(t):
    line = t.lexer.lineno
    print("Character %s not recognized at line %d" % (t.value[0], line))
    t.lexer.skip(1)


## Helper Functions ##

def accentReplace(word):
    identifier = ''
    for i in word:
        index = word.index(i)
        if i in CONST_SPECIAL_CHARACTERS:
            identifier += '_'
        else:
            identifier += i
    return identifier


## Build Lexer ##

# source = open('samplecode.txt', 'r')
#
# lines = source.read()
#
# lines = unicode(lines, 'utf8')

lexer = lex.lex()
inpt_str = """class test{
    public static void main(String[] args) {
        int a = 10;
        int count = 0;
        while (a > count) {
            count = count + 1;
        }
        int b = 0;
        if (a > b) {
            b = a;
        } else {
            b = 10;
        }
    }
}"""
lexer.input(inpt_str)
line_num = 0
program_string = ""
while True:
    tok = lexer.token()
    if not tok:
        break
    else:
        print((tok.value, tok.type))
        k = tok.lineno
        if(line_num!=k):
            line_num = k
            program_string = program_string + ('\n'+str(line_num)+' '+str(tok.value))
        else:
            program_string = program_string + str(tok.value)

def ptry_p(p):
    '''
    start : type_declarations

    type_declarations : type_declaration
                      | type_declarations type_declaration
    
    type_declaration : class_declaration
    class_declaration : class_header class_body

    

    '''


def p_empty(self, p):
        '''empty :'''
print(program_string)