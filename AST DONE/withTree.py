
import ply.yacc as yacc
import re
from symbol_table import *
from lexer import *


root = Tree()
global_symbol_table = {}
current_Node = root
scope = 1
actual_scope = 0
var_list = []

precedence = (
    ('right', 'ASSIGN'),
    ('left','PLUSPLUS','MINUSMINUS'),
    ('left', 'OR'),
    ('left', 'AND'),
    ('left', 'NEQ', 'EQ'),
    ('left', 'GREATER', 'LESS', 'GTEQ', 'LTEQ'),
    ('left', 'ADD', 'SUB'),
    ('left', 'MUL', 'DIV'),
    ('right', 'UMINUS')
)

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


def p_class_declaration(p):
    '''
    class_header_name : modifiers_opt CLASS NAME
    class_declaration : class_header_name class_body
    '''


def p_modifiers_opt(p):
    '''
    modifiers_opt : modifiers 
                  | empty
    modifiers : modifier
              | modifiers modifier
    '''


def p_class_body(p):
    '''
    class_body : opening_bracket classbodydecllist closing_bracket
    tmain : tmain_header opening_bracket method_body closing_bracket
    tmain_header : tmain_name '(' formal_parameter_list_opt ')'
    tmain_name : modifiers_opt type MAIN
    opening_bracket : '{'
    closing_bracket : '}'
    '''
    global actual_scope
    global current_Node
    a = [str(i) for i in p.slice]
    if len(p) == 2 and 'opening_bracket' in a:
        actual_scope = actual_scope + 1
        node = Tree(current_Node)
        current_Node.add_child(node)
        current_Node = node
    if len(p) == 2 and 'closing_bracket' in a:
        actual_scope = actual_scope - 1
        current_Node = current_Node.parent
    #print("main method decl ", p.slice)


def p_classbodydecllist(p):
    '''
    classbodydecllist : classbodydecl 
                      | classbodydecllist classbodydecl
    classbodydecl : method_declaration 
                  | tmain
                  | field_declartaion
    '''

def p_field_declartaion(p):
    '''
    field_declartaion : modifiers_opt type variable_declarators ';'
     '''
    var = str(p[3])
    if var.isalnum():
        current_Node.data[var] = sym_table(var_name = var, var_type = str(p[2]), scope_num = actual_scope)
    #print("Global varible", p.slice, list(p))


def p_method_declaration(p):
    '''
    method_declaration : abstract_method_declaration
                       | method_header opening_bracket method_body closing_bracket
    abstract_method_declaration : method_header ';'
    '''
    #print('p_method decl ', p.slice)
    
def p_method_header(p):
    '''
    method_header : method_header_name '(' formal_parameter_list_opt ')'
    method_header_name : modifiers_opt type NAME 
    method_body : block_statements 
    formal_parameter_list_opt : formal_parameter_list
                              | empty
    formal_parameter_list : formal_parameter
                          | formal_parameter_list ',' formal_parameter
    formal_parameter : type variable_declarator_id   
    variable_declarator_id : NAME 
    '''
    #print('method declaration ', p.slice, list(p))
    if len(p) >= 4:
        print("P4 ", p[3])
    p[0] = p[1]
    a = [str(i) for i in p.slice]
    if len(p) == 3:
        #print("type varible_declarator_id ", p[1], p[2], p.slice)
        var = str(p[2])
        if var.isalnum():
            current_Node.data[var] = sym_table(var_name = var, var_type = str(p[1]), scope_num = actual_scope + 1)
    if 'variable_declarator_id' in a and len(p) == 2:
        if p[1]:
            var_list.append(p[1])

    if len(p) >= 3:
        print("P[1], P[2]", p[1],", ", p[2])
    print("P of 1 ", p[1])

def p_type(p):
    '''type : primitive_type
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
    '''
    block_statements : block_statement
                    | block_statements block_statement
    block_statement : local_variable_declaration_statement
                    | statement
    '''
    p[0] = p[1]
    #print("block statement", p.slice, list(p))

def p_local_variable_declaration(p):
    '''
    local_variable_declaration_statement : local_variable_declaration ';'
    local_variable_declaration : type variable_declarators
                               | modifiers type variable_declarators
    '''
    if len(p) == 3:
        #print("type variable ", p[1], p[2], "slice ", p.slice)
        p[0] = p[2]
        if str(p[2]).isalnum():
            current_Node.data[str(p[2])] = sym_table(var_name = str(p[2]), var_type = str(p[1]), scope_num = actual_scope)


def p_variable_declarations(p):
    '''
    variable_declarators : variable_declarator
                         | variable_declarators ',' variable_declarator
    variable_declarator : variable_declarator_id
                        | variable_declarator_id ASSIGN Expr
    '''
    p[0] = p[1]
    #if len(p) >= 4:
        #if p[2] == '=':
            #print("VAL", p[3])


def p_statement(p):
    '''
    statement : other_statement
              | if_then_statement
              | if_then_else_statement
              | while_statement
              | do_while_statement
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
    if_then_statement : IF '(' expression ')' opening_bracket block_statements closing_bracket
    if_then_else_statement : IF '(' expression ')' opening_bracket block_statements closing_bracket else
    else : ELSE opening_bracket block_statements closing_bracket
    '''
    print('if statement', p.slice)

def p_while_statements(p):
    '''
    while_statement : WHILE '(' expression ')' opening_bracket block_statements closing_bracket
    '''
    print('while statement', p.slice)

def p_do_while_statement(p):
    '''
    do_while_statement : DO opening_bracket block_statements closing_bracket WHILE '(' expression ')' ';'
    '''

def p_expressions(p):
    '''
    expression : assignment_expression
    '''


def p_assignment_expression(p):
    '''
    assignment_expression : assignment
                          | Expr
    assignment : Location assignment_operator Expr
    '''
    print(p.slice)

def p_location(p):
    '''
    Location : name
              | array_access
    '''
def p_assign_op(p):
    '''
    assignment_operator : ASSIGN
                        | TIMES_ASSIGN
                        | DIVIDE_ASSIGN
                        | REMAINDER_ASSIGN
                        | PLUS_ASSIGN
                        | MINUS_ASSIGN
    '''

def p_conditional_expression(p):
    '''
    Expr : exprbinaryexpr
         | unary_expression
         | primary
         | name
    '''
    print(p.slice)

def p_ExprBinaryExpr(p):
    '''exprbinaryexpr : Expr ADD Expr
                      | Expr SUB Expr
                      | Expr MUL Expr
                      | Expr DIV Expr
                      | Expr AND Expr
                      | Expr OR Expr
                      | Expr LESS Expr
                      | Expr LTEQ Expr
                      | Expr GREATER Expr
                      | Expr GTEQ Expr
                      | Expr EQ Expr
                      | Expr NEQ Expr'''
    print(p.slice)

def p_unary_expression(p):
    '''
    unary_expression : pre_increment_expression
                     | pre_decrement_expression
                     | UMINUS Expr %prec UMINUS
                     | post_increment_expression
                     | post_decrement_expression
    '''



def p_pre_expressions(p):
    '''
    pre_increment_expression : PLUSPLUS Expr
    pre_decrement_expression : MINUSMINUS Expr
    '''


def p_post_expressions(p):
    '''
    post_increment_expression : Expr PLUSPLUS
    post_decrement_expression : Expr MINUSMINUS
    '''


def p_primary(p):
    '''
    primary : literal 
            | array_access 
    array_access : name '[' Expr ']'
    '''
    p[0] = p[1]
    #print('primary',p[1])


def p_literal(p):
    '''literal : NUM
               | CHAR_LITERAL
               | STRING_LITERAL
               | TRUE
               | FALSE
               | NULL'''
    p[0] = p[1]
    #print('literal', p[1])




def p_error(p):
    if not p:
        print("EOF")
    else:
       print("error ", p.lineno//2)

if __name__ == '__main__':
    # for testing
    lexer = lex.lex()
    parser = yacc.yacc()

    input_str = """class test{
        int d = 0;
        int c = a*b + a*b ;
        }
    """
    lexer.input(input_str)
    line_num = 0
    program_string = ''
    nwl = 0
    while True:
        tok = lexer.token()
        if not tok:
            break
        else:
            print(tok)
            k = tok.lineno
            if(line_num!=k):
                line_num = k
                program_string = program_string + ('\n'+str(line_num)+' '+str(tok.value))
            else:
                program_string = program_string + ' ' +str(tok.value)

    print(program_string)

    parser.parse(input_str, lexer=lexer)
    #parser.parse(input_str, lexer=lexer ,debug=1)
print(scope)
print('var list ', var_list)
print("SYMBOL TABLE")
print_tree(root)

