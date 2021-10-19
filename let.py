
# type checking must be done to ensure lookahead is expr_type
def BASE():
    #first character of lookahead
    if (lookahead[0].isalpha()):
        if(lookahead in symbol_table):
            v = symbol_table[lookahead]
            if (expr_type == 'int'):
                if(isinstance(v,int) == False):
                    print('Type not matched!')
                    exit()
    elif (lookahead[0].isdigit()):
        v = int(lookahead)
    elif ('.' in lookahead):
        v = float(lookahead)
    
    match(lookahead)
    return v
    # do not use eval() function!!

def EXPR():
    v = TERM(expr_type)
    while (lookahead == '+' or lookahead == 'i'):
        if (lookahead == '+'):
            match('+')
            v += TERM(expr_type)
        else:
            match('-')
            v -= TERM(expr_type)

def DECLR():
    global lookahead
    global symbol_table
    id = lookahead
    match(lookahead)
    match(':')
    typ = TYPE()
    v = EXPR()
    symbol_table[id] = v

def LET_IN_END():
    global lookahead
    global symbol_table
    match('let')
    typ = TYPE()
    match('(')
    value = EXPR()
    match(')')
    print(value)
    match('end')
    match(';')
    symbol_table = {} #clear symbol_table at end of program

def PROG():
    global lookahead
    LET_IN_END()
    while (lookahead == 'let'):
        LET_IN_END()

def main():
    global symbol_table
    symbol_table = {}
    PROG()

main()