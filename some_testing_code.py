    global scope
    try:
        print(p.slice, p.stack, p.lexpos)
        a = [str(i) for i in p.slice]
        if 'variable_declarator_id' in a:
            print("variable ", p[1])
        print("ALL ATTRIBUTES OF P OBJECT\n", dir(p))
        if (p[5] == '{' or p[9] == '{'):
            scope = scope + 1
        print('SCOPE in opening statement ', scope)
        if (p[7] == '}' or p[11] == '}'):
            scope = scope - 1
        print("SCOPE ", scope)
    except Exception as e:
        print(e)