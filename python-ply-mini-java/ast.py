
class Node:
    pass

class Iden(Node):
    def __init__(self, name, lineno):
        self.name = name
        self.lineno = lineno

    def show(self):
        print ('id')

class NullNode(Node):
    def __init__(self):
        self.type = 'void'

    def is_null(self):
        return True

    def show(self):
        print ('null node')

class Program(Node):
    def __init__(self, ClassDeclList):
        self.ClassDeclList = ClassDeclList
        self.name = 'Program'

    def show(self):
        print 'Program => ClassDeclList'
        self.ClassDeclList.show()

class ClassDeclList(Node):
    def __init__(self, ClassDecl, ClassDeclList):
        self.ClassDecl = ClassDecl
        self.ClassDeclList = ClassDeclList
        self.name = 'ClassDeclList'

    def show(self):
        print 'ClassDeclList => ClassDecl ClassDeclList'
        self.ClassDecl.show()
        self.ClassDeclList.show()

class ClassDecl(Node):
    def __init__(self, Iden, ExtendClass, FieldMethDecl):
        self.name = Iden
        self.ExtendClass = ExtendClass
        self.FieldMethDecl = FieldMethDecl
        self.name = 'ClassDecl'

    def show(self):
        print 'ClassDecl => CLASS IDEN ExtendClass LEFTBRACE FieldMethDecl RIGHTBRACE'
        self.ExtendClass.show()
        self.FieldMethDecl.show()

class ExtendClass(Node):
    def __init__(self, IDEN):
        self.iden = IDEN
        self.name = 'ExtendClass'

    def show(self):
        print 'ExtendClass => EXTENDS IDEN'

class FieldMethDecl(Node):
    def __init__(self, FieldMeth, FieldMethDecl):
        self.FieldMeth = FieldMeth
        self.FieldMethDecl = FieldMethDecl
        self.name = 'FieldMethdDecl'

    def show(self):
        print 'FieldMethDecl => FieldMeth FieldMethDecl'

class FieldMeth(Node):
    def __init__(self, FieldMeth):
        self.FieldMeth = FieldMeth
        self.name = 'FieldMethd'

    def show(self):
        print  'FieldMeth => FieldDecl | MethDecl'

class FieldDecl(Node):
    def __init__(self, Type, IDEN, IdenCommaList):
        self.Type = Type
        self.IDEN = IDEN
        self.IdenCommaList = IdenCommaList

    def show(self):
        print 'FieldDecl => Type IDEN IdenCommaList SEMICOLON'
        self.type.type()
        self.iden.show()
        self.IdenCommaList.show()

class IdenCommaList(Node):
    def __init__(self, IdenComma, IdenCommaList):
        self.IdenComma = IdenComma
        self.IdenCommaList = IdenCommaList
        self.name = 'IdenCommaList'

    def swho(self):
        print 'FieldDecl => Type IDEN IdenCommaList SEMICOLON'

class IdenComma(Node):
    def __init__(self, IDEN):
        self.IDEN = IDEN
        self.name = 'IdenComma'

    def show(self):
        print 'IdenComma => COMMA IDEN'

