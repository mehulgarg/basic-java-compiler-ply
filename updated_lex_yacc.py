import ply.lex as lex
import ply.yacc as yacc
import re
from symbol_table import sym_table

gobal_symbol_table = {}
scope = 1
var_list = []
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
            'String'
            )
tokens = [
    'NAME',
    'NUM',
    'CHAR_LITERAL',
    'STRING_LITERAL',

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

print("Starting parsing")

def p_start(p):
    '''start : type_declarations
    '''
    print("start ")

def p_type_declarations(p):
    '''
    type_declarations : type_declaration
                      | type_declarations ',' type_declaration
    
    type_declaration : class_declaration
    '''
    print("type decl ", p.slice)


def p_class_declaration(p):
    '''
    class_header_name : modifiers_opt CLASS NAME
    class_declaration : class_header_name class_body
    '''
    print("class declaration", p.slice)


def p_modifiers_opt(p):
    '''
    modifiers_opt : modifiers 
                  | empty
    modifiers : modifier
              | modifiers modifier
    '''
    print("modifiers", p.slice)


def p_class_body(p):
    '''
    class_body : '{' classbodydecllist '}'
    tmain : modifiers_opt type MAIN '(' formal_parameter_list_opt ')' method_body
    '''
    print("class body", p.slice)


def p_classbodydecllist(p):
    '''
    classbodydecllist : classbodydecl 
                      | classbodydecllist ',' classbodydecl
    classbodydecl : method_declaration 
                  | tmain
    '''
    print("main method", p.slice)

def p_method_declaration(p):
    '''
    method_declaration : abstract_method_declaration
                       | method_header method_body
    abstract_method_declaration : method_header ';'
    '''
    print("method", p.slice)


def p_method_header(p):
    '''
    method_header : method_header_name '(' formal_parameter_list_opt ')'
    method_header_name : modifiers_opt type NAME 
    method_body : '{' block_statements '}'
    formal_parameter_list_opt : formal_parameter_list
                              | empty
    formal_parameter_list : formal_parameter
                          | formal_parameter_list ',' formal_parameter
    formal_parameter : type variable_declarator_id   
    variable_declarator_id : NAME 
    type : primitive_type
         | array_type
    array_type : primitive_type dims
               | name dims
    dims : '[' ']'
         | dims '[' ']' 
    primitive_type : BOOLEAN
                   | VOID
                   | BYTE
                   | SHORT
                   | INT
                   | LONG
                   | CHAR
                   | FLOAT
                   | DOUBLE 
                   | STRING
    '''
    if len(p) >= 4:
        print("P4 ", p[3])
    p[0] = p[1]
    a = [str(i) for i in p.slice]
    if 'variable_declarator_id' in a and len(p) == 2:
        if p[1]:
            var_list.append(p[1])
    
    
    global scope
    try:
        if (p[1] == '{'):
            print("opening bracket")
            scope = scope + 1
        if (p[3] == '}'):
            print('closing bracket')
            scope = scope - 1
    except :
        print("exception in method header")
    print("Scope ", scope)

    if len(p) >= 3:
        print("P[1], P[2]", p[1],", ", p[2])
    print("P of 1 ", p[1])


def p_modifier_type(p):
    '''modifier : PUBLIC
                | PROTECTED
                | PRIVATE
                | STATIC
                | ABSTRACT
                | FINAL
                | NATIVE
    '''


def p_name(p):
    '''name : simple_name
            | qualified_name
    simple_name : NAME
    qualified_name : name '.' simple_name'''


def p_empty(p):
    
    '''empty :'''


def p_block(p):
    '''block_statements : block_statement
                        | block_statements block_statement
    block_statement : local_variable_declaration_statement
                    | statement
    '''
    p[0] = p[1]

def p_local_variable_declaration(p):
    '''
    local_variable_declaration_statement : local_variable_declaration ';'
    local_variable_declaration : type variable_declarators
                               | modifiers type variable_declarators
    '''
    if len(p) == 3:
        print("type variable ", p[1], p[2], "slice ", p.slice)
        p[0] = p[2]
        if str(p[2]).isalnum():
            gobal_symbol_table[str(p[2])] = sym_table(var_name = str(p[2]), var_type = str(p[1]))


def p_variable_declarations(p):
    '''
    variable_declarators : variable_declarator
                         | variable_declarators ',' variable_declarator
    variable_declarator : variable_declarator_id
                        | variable_declarator_id '=' variable_initializer
    variable_initializer : primary
    '''
    p[0] = p[1]
    if len(p) >= 4:
        if p[2] == '=':
            print("VAL", p[3])


def p_statement(p):
    '''
    statement : other_statement
              | if_then_statement
              | if_then_else_statement
              | while_statement
    '''


def p_other_statement(p):
    '''
    other_statement : expression_statement
                    | break_statement
                    | return_statement
                    | continue_statement
                    | ';'
    '''


def p_expression_statement(p):
    '''
    expression_statement : statement_expression ';'
    statement_expression : assignment
                         | unary_expression
                         | method_invocation
    '''


def p_method_invocation(p):
    '''
    method_invocation : NAME '(' argument_list ')'
                      | NAME '(' ')'
    '''


def p_argument_list(p):
    '''
    argument_list : expression
                  | argument_list ',' expression
    '''


def p_break_statement(p):
    '''
    break_statement : BREAK ';'
                    | BREAK NAME ';'
    '''


def p_return_statement(p):
    '''
    return_statement : RETURN expression_opt ';'
    expression_opt : expression
                   | empty
    '''
def p_continue_statement(p):
    '''
    continue_statement : CONTINUE ';'
    '''


def p_if_statements(p):
    '''
    if_then_statement : IF '(' expression ')' '{' block_statements '}'
    if_then_else_statement : IF '(' expression ')' '{' block_statements '}' ELSE '{' block_statements '}'
    '''


def p_while_statements(p):
    '''
    while_statement : WHILE '(' expression ')' '{' block_statements '}'
    '''


def p_expressions(p):
    '''
    expression : assignment_expression
    '''


def p_assignment_expression(p):
    '''
    assignment_expression : assignment
                          | conditional_expression
    assignment : postfix_expression assignment_operator assignment_expression
    '''

def p_assign_op(p):
    '''
    assignment_operator : '='
                        | TIMES_ASSIGN
                        | DIVIDE_ASSIGN
                        | REMAINDER_ASSIGN
                        | PLUS_ASSIGN
                        | MINUS_ASSIGN
    '''


def p_conditional_expression(p):
    '''
    conditional_expression : conditional_or_expression 
    conditional_or_expression : conditional_and_expression
                              | conditional_or_expression OR conditional_and_expression
    conditional_and_expression : inclusive_or_expression
                               | conditional_and_expression AND inclusive_or_expression
    '''

def p_and_or_expressions(p):
    '''
    inclusive_or_expression : and_expression
                            | inclusive_or_expression '|' and_expression
    and_expression : equality_expression
                   | and_expression '&' equality_expression
    '''

def p_equality_expression(p):
    '''
    equality_expression : equality_expression EQ relational_expression
                        | equality_expression NEQ relational_expression
                        | relational_expression
    '''
    
def p_relational_expression(p):
    '''
    relational_expression : additive_expression
                          | relational_expression '>' additive_expression
                          | relational_expression '<' additive_expression
                          | relational_expression GTEQ additive_expression
                          | relational_expression LTEQ additive_expression
    '''


def p_additive_expression(p):
    '''
    additive_expression : multiplicative_expression
                        | additive_expression '+' multiplicative_expression
                        | additive_expression '-' multiplicative_expression
    '''


def p_multiplicative_expression(p):
    '''
    multiplicative_expression : unary_expression
                              | multiplicative_expression '*' unary_expression
                              | multiplicative_expression '/' unary_expression
                              | multiplicative_expression '%' unary_expression
    '''
    p[0] = p[1]

def p_unary_expression(p):
    '''
    unary_expression : pre_increment_expression
                     | pre_decrement_expression
                     | '+' unary_expression
                     | '-' unary_expression
                     | postfix_expression
    '''



def p_pre_expressions(p):
    '''
    pre_increment_expression : PLUSPLUS unary_expression
    pre_decrement_expression : MINUSMINUS unary_expression
    '''


def p_post_expressions(p):
    '''
    postfix_expression : primary
                       | name
                       | post_increment_expression
                       | post_decrement_expression
    post_increment_expression : postfix_expression PLUSPLUS
    post_decrement_expression : postfix_expression MINUSMINUS
    '''


def p_primary(p):
    '''
    primary : literal 
            | array_access 
    array_access : name '[' expression ']'
    '''
    p[0] = p[1]
    print('primary',p[1])


def p_literal(p):
    '''literal : NUM
               | CHAR_LITERAL
               | STRING_LITERAL
               | TRUE
               | FALSE
               | NULL'''
    p[0] = p[1]
    print('literal', p[1])




def p_error(p):
    if not p:
        print("EOF")
    else:
       print("error ", p)

if __name__ == '__main__':
    # for testing
    lexer = lex.lex()
    parser = yacc.yacc()

    input_str = """
    class test{
        public static void main(String[] args) {
            int d = 0;
            int a = 10;
            int count = 0;
            while (a > count) {
                int k = 0;
                count = count + 1;
            }
            int b = 0;
            if (a > b) {
                b = a;
            } else {
                b = 10;
            }
        
        }
        static int hello(int d){
            int k = 0;
        }
    }   
    """
    lexer.input(input_str)
    for token in lexer:
        print(token)
    parser.parse(input_str, lexer=lexer)
    # parser.parse(input_str, lexer=lexer ,debug=1)
print(scope)
print('var list ', var_list)
print(gobal_symbol_table)

