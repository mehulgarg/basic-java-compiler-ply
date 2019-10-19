import ply.yacc as yacc
import os
from lexer import *
from ast import *

precedence = (
    ('right', 'ASSIGNMENT'),
    ('left', 'OR'),
    ('left', 'AND'),
    ('left', 'NOTEQUAL', 'EQUAL'),
    ('left', 'GREATER', 'LESS', 'GREATEREQUAL', 'LESSEQUAL'),
    ('left', 'ADDITION', 'SUBSTRACTION', 'CONCAT'),
    ('left', 'MULTIPLICATION', 'DIVISION', 'MODULO'),
    ('right','NEW', 'NOT','UMINUS'),
    ('left', 'DOT')
)

##########################
# program ::= classDecl* #
##########################
def p_Program(p):
    'Program : ClassDeclList'
    p[0] = Program(p[1])

def p_ClassDeclList(p):
    'ClassDeclList : ClassDecl ClassDeclList'
    p[0] = ClassDeclList(p[1], p[2])

def p_ListaClassDecl1(p):
    'ClassDeclList : empty'
    p[0] = NullNode()

#####################################################################
# classDecl ::= class id[extend id] '{' (fieldDecl | methDecl)* '}' #
#####################################################################

def p_ClassDecl(p):
    'ClassDecl : CLASS IDEN ExtendClass LEFTBRACE FieldMethDecl RIGHTBRACE'
    p[0] = ClassDecl(Iden(p[2],p.lineno(1)), p[3], p[5])

## ExtendClas can be empty ##

def p_ExtendClass(p):
    'ExtendClass : EXTENDS IDEN'
    p[0] = ExtendClass(Iden(p[2],p.lineno(1)))

def p_ExtendClass1(p):
    'ExtendClass : empty'
    p[0] = NullNode()

def p_FieldMethDecl(p):
    'FieldMethDecl : FieldMeth FieldMethDecl'
    p[0] = FieldMethDecl(p[1],p[2])

def p_FieldMethDecl1(p):
    'FieldMethDecl : empty'
    p[0] = NullNode()

def p_FieldMeth(p):
    '''FieldMeth : FieldDecl
                 | MethDecl'''
    p[0] = FieldMeth(p[1])

######################################
# fieldDecl ::=type id( ',' id)* ';' #
######################################

def p_FieldDecl(p):
    'FieldDecl : Type IDEN IdenCommaList SEMICOLON'
    p[0] = FieldDecl(p[1], Iden(p[2], p.lineno(1)), p[3])

def p_IdenCommaList(p):
    'IdenCommaList : IdenComma IdenCommaList'
    p[0] = IdenCommaList(p[1], p[2])

def p_IdenCommaList1(p):
    'IdenCommaList : empty'
    p[0] = NullNode()

def p_IdenComma(p):
    'IdenComma : COMMA IDEN'
    p[0] = IdenComma(Iden(p[2],p.lineno(1)))

#########################################################
# methDecl ::= (type | void) id '(' [formals] ')' block #
#########################################################

def p_MethDecl(p):
    'MethDecl : MethType IDEN LEFTPARENT Args RIGHTPARENT Block'
    #p[0] = MethDecl(p[1],Id(p[2],p.lineno(1)),p[4],p[6])
    pass

def p_MethType(p):
    'MethType : Type'
    #p[0] = MethType(p[1])
    pass

def p_MethdType1(p):
    'MethType : VOID'
    #p[0] = MethType(p[1])
    pass

def p_Args(p):
    '''Args : Formals
            | empty'''
    #p[0] = Args(p[1])
    pass

########################################
#  formals ::= type id ( ',' type id)* #
########################################

def p_Formals(p):
    'Formals : Type IDEN IdenTypeCommaList'
    #p[0] = Formals(p[1],Id(p[2],p.lineno(1)),p[3])
    pass

def p_IdenTypeCommaList(p):
    'IdenTypeCommaList : CommaTypeId IdenTypeCommaList'
    #p[0] = IdenTypeCommaList(p[1],p[2])
    pass

def p_IdenTypeCommaList1(p):
    'IdenTypeCommaList : empty'
    #p[0] = NullNode(' ')
    pass

def p_CommaTypeId(p):
    'CommaTypeId : COMMA Type IDEN'
    #p[0] = CommaTypeId(p[2],Id(p[3],p.lineno(1)))
    pass

##########################################################
# type ::= int | boolean | string | id | type '[' ']' id #
##########################################################

def p_Type(p):
    '''Type : INT
            | BOOLEAN
            | STRING
            | IDEN
            | Array'''
    #p[0] = Type(p[1])
    pass

def p_Array(p):
    'Array : Type LEFTSQRBRACKET RIGHTSQRBRACKET'
    #p[0] = Array(p[1])
    pass


####################################
# block ::= '{' varDecl* stmt* '}' #
####################################

def p_Block(p):
    'Block : LEFTBRACE VarDeclList StmtList RIGHTBRACE'
    #p[0] = Block(p[2],p[3])
    pass

def p_StmtList(p):
    'StmtList : Stmt StmtList'
    #p[0] = StmtList(p[1],p[2])
    pass

def p_StmtList1(p):
    'StmtList : empty'
    #p[0] = NullNode(' ')
    pass

#############################################################
# varDecl ::= type id ['=' expr] ( ',' id ['=' expr] )* ';' #
#############################################################

def p_VarDeclList(p):
    'VarDeclList : Type IDEN ExpDecl ExpDeclList SEMICOLON VarDeclList'
    #p[0] = VarDecl(p[1],p[2],p[3],p[4])
    pass

def p_VarDeclList1(p):
    'VarDeclList : empty'

def p_ExpDeclList(p):
    'ExpDeclList : CommaExpDecl ExpDeclList'
    #p[0] = ExpDeclList(p[1],p[2])
    pass

def p_ExpDeclList1(p):
    'ExpDeclList : empty'
    #p[0] = NullNode('')
    pass

def p_CommaExpDecl(p):
    'CommaExpDecl : COMMA IDEN ExpDecl'
    #p[0] = CommaExpDecl(Id(p[2],p.lineno(1)), p[3])
    pass

def p_Decl(p):
    'ExpDecl : ASSIGNMENT Expr'
    #p[0] = Decl(p[2])
    pass

def p_Decl1(p):
    'ExpDecl : empty'
    #p[0] = NullNode(' ')
    pass

#######################################
# stmt ::= assign ';'                 #
#  | call ';'                         #
#  | return [expr] ';'                #
#  | if '(' expr ')' stmt [else stmt] #
#  | while '(' expr ')' stmt          #
#  | break ';' | continue ';'         #
#  | block                            #
#######################################

def p_Stmt(p):
    '''Stmt : Assign SEMICOLON
            | Call SEMICOLON
            | Return
            | IfStmt
            | WhileStmt
            | BREAK SEMICOLON
            | CONTINUE SEMICOLON
            | Block'''
    #p[0] = Stmt(p[1])
    pass


## Assign SEMICOLON ##

################################
# assign ::= location '=' expr #
################################

def p_Assign(p):
    'Assign : Location ASSIGNMENT Expr'

############################################
# location ::= id|expr '.' id|expr '[' ']' #
############################################

def p_Location(p):
    'Location : IDEN'

def p_Location1(p):
    'Location : Expr DOT IDEN'

def p_Location2(p):
    'Location : Expr LEFTSQRBRACKET Expr RIGHTSQRBRACKET'

## Call SEMICOLON ##

#####################################
# call ::= method '(' [actuals] ')' #
#####################################

def p_Call(p):
    'Call : Method LEFTPARENT Actuals RIGHTPARENT'
    pass

#############################
# method ::= id|expr '.' id #
#############################

def p_Method(p):
    'Method : IDEN'

def p_Method1(p):
    'Method : Expr DOT IDEN'

#################################
# actuals ::= expr (',' expr )* #
#################################

# La gramatica no permite hacer llamados sin argumentos ?

def p_Actuals(p):
    'Actuals : Expr ExprCommaList'

def p_ExprCommaList(p):
    'ExprCommaList : ExprComma ExprCommaList'

def p_ExprCommaList1(p):
    'ExprCommaList : empty'

def p_ExprComma(p):
    'ExprComma : COMMA Expr'

## Return ##

#####################
# return [expr] ';' #
#####################

def p_Return(p):
    'Return : RETURN ReturnExpr SEMICOLON'
    #p[0] = OtherReturn(p[2])
    pass

def p_ReturnExpr(p):
    'ReturnExpr : Expr'
    #p[0] = OtherExpr(p[1])
    pass

def p_ReturnExpr1(p):
    'ReturnExpr : empty'
    #p[0] = NullNode('')
    pass


## IfStmt ##

####################################
# if '(' expr ')' stmt [else stmt] #
####################################

def p_IfStmt(p):
    'IfStmt : IF LEFTPARENT Expr RIGHTPARENT Stmt ElseStmt'

def p_ElseStmt(p):
    'ElseStmt : ELSE Stmt'
    #p[0] = ElseStmt(p[2])
    pass

def p_ElseStmt1(p):
    'ElseStmt : empty'
    #p[0] = NullNode(' ')
    pass

## WhileStmt ##

###########################
# while '(' expr ')' stmt #
###########################

def p_WhileStmt(p):
    'WhileStmt : WHILE LEFTPARENT Expr RIGHTPARENT Stmt'

############################
# expr ::= location        #
#  | call                  #
#  | this                  #
#  | new id '(' ')'        #
#  | new type '[' expr ']' #
#  | expr '.' length       #
#  | expr binary expr      #
#  | unary expr            #
#  | literal               #
#  | '(' expr ')'          #
############################

def p_Expr(p):
    '''Expr : Location
            | Call
            | THIS
            | NewId
            | NewTypeExpr
            | ExprLength
            | ExprBinaryExpr
            | UnaryExpr
            | Literal
            | Number
            | ParentExprParent'''
    #p[0] = Expr(p[1])
    pass


## NewId ##

##################
# new id '(' ')' #
##################

def p_NewId(p):
    'NewId : NEW IDEN LEFTPARENT RIGHTPARENT'
    #p[0] = NewId(Id(p[2],p.lineno(1)))
    pass

## NewTypeExpr ##

#########################
# new type '[' expr ']' #
#########################

def p_NewTypeExpr(p):
    'NewTypeExpr : NEW Type LEFTSQRBRACKET Expr LEFTSQRBRACKET'
    #p[0] = NewTypeExpr(p[2], p[4])
    pass

## ExprLength ##

###################
# expr '.' length #
###################

def p_ExprLength(p):
    'ExprLength : Expr DOT LENGTH'

## ExprBinaryExpr ##

####################
# expr binary expr #
####################

def p_ExprBinaryExpr(p):
    '''ExprBinaryExpr : Expr ADDITION Expr
                      | Expr SUBSTRACTION Expr
                      | Expr MULTIPLICATION Expr
                      | Expr DIVISION Expr
                      | Expr MODULO Expr
                      | Expr AND Expr
                      | Expr OR Expr
                      | Expr CONCAT Expr
                      | Expr LESS Expr
                      | Expr LESSEQUAL Expr
                      | Expr GREATER Expr
                      | Expr GREATEREQUAL Expr
                      | Expr EQUAL Expr
                      | Expr NOTEQUAL Expr'''
    #p[0] = Binop(p[1], p[3])
    pass

###########################################################
## binary ::= '+' | '-' | '*' | '/' | '%' | '&&' | '||'   #
##                | '<' | '<=' | '>' | '>=' | '==' | '!=' #
###########################################################

## UnaryExpr ##

#######################
# unary ::= '-' | '!' #
#######################

def p_UnaryExpr(p):
    '''UnaryExpr : UnaryMinus
                 | NOT'''
    #p[0] = UnaryExpr(p[1],p[2])
    pass

def p_UnaryMinus(p):
    'UnaryMinus : SUBSTRACTION Expr %prec UMINUS'

## Literal ##

######################################################################
# literal ::= integer-literal | string-literal | true | false | null #
######################################################################

def p_Literal(p):
    '''Literal : INT
               | STRING
               | TRUE
               | FALSE
               | NULL'''

def p_ParentExprParent(p):
    'ParentExprParent : LEFTPARENT Expr RIGHTPARENT'

def p_Number(p):
    '''Number : CIENTIFIC
              | HEXADEC

              | NUMBER
              | BINARY
              | FLOAT'''

def p_empty(p):
    'empty : '


def p_error(error):
    print("Syntax Error: Unexpected '%s', near line '%s' " % (error.value, error.lineno) )

yacc.yacc(method='SLR')

tests = os.path.dirname(os.path.realpath('__file__')) + "/tests/"

file = open(os.path.join(tests, "test_multi_class.mj"), "r" ).read()

file = unicode(file, 'utf8')

# Se construye el ast: raiz=p[0] de la primera regla
raiz = yacc.parse(file)

raiz.show()