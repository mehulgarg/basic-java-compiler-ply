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