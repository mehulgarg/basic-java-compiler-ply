class sym_table():
    def __init__(self, var_name, scope_num = 0, val = 'none', var_type = 'none'):
        self.var_name = var_name
        self.scope_num = scope_num
        self.val = val
        self.var_type = var_type

    def __repr__(self):
        return "var_name: {0}, scope_num: {1}, val: {2}, var_type: {3}".format(self.var_name, self.scope_num, self.val, self.var_type)

    def __str__(self):
        return "Variable([{0},{1},{2},{3}])".format(self.var_name, self.scope_num, self.val, self.var_type)

class Tree(object):
    "Generic tree node."
    def __init__(self,parent=None,children=None):
        self.data = {}
        self.parent = parent
        if parent == None:
            self.scope = '0'
        else:
            self.scope = parent.scope + '.' + str(parent.no_of_children+1)
        self.no_of_children = 0
        self.children = []
        if children is not None:
            for child in children:
                self.add_child(child)
    
    def add_child(self, node):
        assert isinstance(node, Tree)
        self.children.append(node)
        self.no_of_children = self.no_of_children + 1

def print_tree(node):
    if node.no_of_children == 0:
        print(node.scope)
        print(node.data)
        return
    else:
        print(node.scope)
        print(node.data)
        for i in range(node.no_of_children):
            print_tree(node.children[i])
        return