import ply.lex as lex
import ply.yacc as yacc
import re

variable_list = []

keywords = (            
            'import', 
            'package',
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
            'null'
            )
tokens = [
    'NAME',
    'NUM',
    'CHAR_LITERAL',
    'STRING_LITERAL',
    'LINE_COMMENT',

    'OR', 'AND',
    'EQ', 'NEQ', 'GTEQ', 'LTEQ',

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
    t.lexer.lineno += t.value.count('\n')

t_OR = r'\|\|'
t_AND = '&&'

t_EQ = '=='
t_NEQ = '!='
t_GTEQ = '>='
t_LTEQ = '<='
t_TIMES_ASSIGN = r'\*='
t_DIVIDE_ASSIGN = '/='
t_REMAINDER_ASSIGN = '%='
t_PLUS_ASSIGN = r'\+='
t_MINUS_ASSIGN = '-='

t_PLUSPLUS = r'\+\+'
t_MINUSMINUS = r'\-\-'

t_ignore = ' \t\f'

def t_NAME(t):
    '[A-Za-z_$][A-Za-z0-9_$]*'
    if t.value in keywords:
        t.type = t.value.upper()
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")

def t_error(t):
    print("Illegal character '{}' ({}) in line {}".format(t.value[0], hex(ord(t.value[0])), t.lexer.lineno))
    t.lexer.skip(1)

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

print(program_string)

def p_start(p):
    '''start : type_declarations
    type_declarations : type_declaration
                      | type_declarations ',' type_declaration
    
    type_declaration : class_declaration
    class_declaration : class_header_name class_body
    class_header_name : modifiers_opt CLASS NAME
    modifiers_opt : modifiers 
                  | empty
    modifiers : modifier
              | modifiers modifier
    
    class_body : '{' classbodydecllist '}'
    tmain : modifiers_opt type MAIN '(' formal_parameter_list_opt ')' method_body 
          | modifiers_opt VOID MAIN '(' formal_parameter_list_opt ')' method_body
    classbodydecllist : classbodydecl 
                      | classbodydecllist ',' classbodydecl
    classbodydecl : method_declaration 
                  | STATIC block_statements 
                  | tmain
    method_declaration : abstract_method_declaration
                       | method_header method_body
    abstract_method_declaration : method_header ';'
    method_header : method_header_name formal_parameter_list_opt ')'
    method_header_name : modifiers_opt type NAME '(' 
    method_body : '{' block_statements '}'
    formal_parameter_list_opt : formal_parameter_list
                              | empty
    formal_parameter_list : formal_parameter
                          | formal_parameter_list ',' formal_parameter
    formal_parameter : type variable_declarator_id   
    variable_declarator_id : NAME 
                           | variable_declarator_id '[' ']' '''
    

def p_modifier_type(p):
    '''modifier : PUBLIC
                | PROTECTED
                | PRIVATE
                | STATIC
                | ABSTRACT
                | FINAL
                | NATIVE
                | VOID
    type : primitive_type
         | array_type
    primitive_type : BOOLEAN
                   | VOID
                   | BYTE
                   | SHORT
                   | INT
                   | LONG
                   | CHAR
                   | FLOAT
                   | DOUBLE 
    array_type : primitive_type dims
               | name dims
    dims : '[' ']'
         | dims '[' ']' '''
    variable_list.append(p)
def p_name(p):
    '''name : simple_name
            | qualified_name
    simple_name : NAME
    qualified_name : name '.' simple_name'''
    

    variable_list.append(p)

def p_empty(p):
    '''empty :'''



def p_block(p):
    '''block_statements : block_statement
                        | block_statements block_statement
    block_statement : local_variable_declaration_statement
                    | statement
    local_variable_declaration_statement : local_variable_declaration ';'
    local_variable_declaration : type variable_declarators
                               | modifiers type variable_declarators
    variable_declarators : variable_declarator
                         | variable_declarators ',' variable_declarator
    variable_declarator : variable_declarator_id
                        | variable_declarator_id '=' variable_initializer
    variable_initializer : expression
    statement : other_statement
              | if_then_statement
              | if_then_else_statement
              | while_statement
    other_statement : expression_statement
                    | break_statement
                    | return_statement
                    | continue_statement
                    | ';'
    continue_statement : CONTINUE ';'
    expression_statement : statement_expression ';'
    statement_expression : assignment
                         | increment_expression
                         | decrement_expression
                         | method_invocation
    method_invocation : NAME '(' argument_list ')'
                      | NAME '(' ')'
    argument_list : expression
                  | argument_list ',' expression

    if_then_statement : IF '(' expression ')' '{' statement '}'
    if_then_else_statement : IF '(' expression ')' '{' statement '}' ELSE '{' statement '}'
    while_statement : WHILE '(' expression ')' '{' statement '}'
    break_statement : BREAK ';'
                    | BREAK NAME ';'
    return_statement : RETURN expression_opt ';'
    expression_opt : expression
                    | empty'''
    variable_list.append(p)

def p_expressions(p):
    '''expression : assignment
                  | conditional_expression
    assignment : name assignment_operator expression
    conditional_expression : arithematic_expression
                           | relational_expression
                           | other_expression
                           | primary
    relational_expression : relational_expression '>' relational_expression
                          | relational_expression '<' relational_expression
                          | relational_expression GTEQ relational_expression
                          | relational_expression LTEQ relational_expression 
                          | relational_expression NEQ relational_expression   
                          | relational_expression EQ relational_expression
                          | primary

    arithematic_expression : additive_expression

    additive_expression : additive_expression '+' multiplicative_expression
                        | additive_expression '-' multiplicative_expression
                        | primary

    multiplicative_expression : multiplicative_expression '*' unary_expression
                              | multiplicative_expression '/' unary_expression
                              | multiplicative_expression '%' unary_expression
                              | primary

    unary_expression : increment_expression
                       | decrement_expression
                       | '+' unary_expression
                       | '-' unary_expression
                       | primary

    increment_expression : PLUSPLUS unary_expression
                         | unary_expression PLUSPLUS

    decrement_expression : MINUSMINUS unary_expression
                         | unary_expression MINUSMINUS
    
    primary : name 
            | literal

    other_expression : expression otherop expression
    '''
    variable_list.append(p)

def p_operator(p):
    '''assignment_operator : '='
                           | TIMES_ASSIGN
                           | DIVIDE_ASSIGN
                           | REMAINDER_ASSIGN
                           | PLUS_ASSIGN
                           | MINUS_ASSIGN
    otherop : AND
            | OR
            | '&'
            | '|'
    '''
    
    variable_list.append(p)
    print(":FUCJKSKFJLKJLKSAJ")
def p_literal(p):
    '''literal : NUM
               | CHAR_LITERAL
               | STRING_LITERAL
               | TRUE
               | FALSE
               | NULL'''
    print("literal")



def p_error(p):
    pass



yacc.yacc()
input_str = """class test{
    public static void main(String[] args) {
        int a = 10;
        int count = 0;
        while (a > count) {
            count = count + 1;
        }
        int b = 0;
        int c = 0;
        if (a > b) {
             if(a == b) {
                 b = c;
             }
            b = a;
        } else {
            b = 10;
            j
        }
    }
}"""
for i in input_str :
    yacc.parse(i)

print("Variable List ", variable_list)