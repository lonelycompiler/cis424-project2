#!/usr/bin/python3
# Gopal Shukla
# Benjamin Ward 2730444
# CIS 424 Section 50
# Prof. Sang
# October 21, 2021

# Project 2 Objectives:
# This project is an interpreter which uses the TDRD method and synthesized attributes to parse
# and evaluate a simple strong-typed programming language (tiny). The language is defined below:
# 
# <prog> ::= <let-in-end> { <let-in-end> }
# <let-in-end> ::= let <decl-list> in <type>  (<expr> ) end ;
# <decl-list> ::= <decl> { <decl> }
# <decl> ::= id : <type> = <expr> ;
# <type> ::= int | real
# <expr> ::= <term> { + <term> | - <term> }
# <term> ::= <factor> { * <factor> | / <factor> }
# <factor> ::= <base> ^ <factor> | <base>
# <base> ::= ( <expr> ) | id | number | <type> ( id )
#
# terminal characters are space delimited and the input file name is given from cmd

#!/usr/bin/python3
# chmod +x let.py
# do not use eval() function!!


import sys

# This method tries to obtain the next mitr from the input file, if it fails it returns ''
def lexan():
    global mitr
    try:
        return next(mitr)
    except StopIteration:
        return ''

# This method compares ch to the lookahead and if they are equal, it sets lookahead to 
# the next iterable by calling lexan(). Otherwise, it prints error.
def match(ch):
    global lookahead
    if(ch == lookahead):
        lookahead = lexan()
    else:
        print('Error')
        exit()

# This method is the first one called when evaluating the grammar. It calls LET_IN_END() and 
# then while lookahead is "let" it continues to call LET_IN_END()
def PROG():
    global lookahead
    LET_IN_END()
    while lookahead == 'let':
        LET_IN_END()
   
# This method matches 'let', calls DECL_LIST(), matches 'in', assigns typ to the type of the current lookahead, then
# matches '(', and puts the result of the expression into the list of results of all programs for the input file (to be
# displayed later in main), and finally matches the remaining terminals ')' 'end' ';', before clearing the symbol table.
def LET_IN_END():
    global lookahead
    global symbol_table
    global result
    match('let')
    DECL_LIST()
    match('in')

    typ = TYPE(lookahead)

    match('(')
    result.append(str(EXPR()))
    match(')')
    match('end')
    match(';')
    symbol_table = {} #clear symbol_table at end of program

# This method calls DECL() amd while the lookahead is not 'in', it continues to call DECL().
# We check if it matches 'in' or not because there may be multiple IDs defined with values.
def DECL_LIST():
    global lookahead
    DECL()
    while lookahead != 'in':
        DECL()

# This method sets the ID to lookahead, matches the ID and ':', then sets typ to the type of 
# the current lookahead, maches '=', sets the symbol table's value for the ID to its expression,
# and finally matches ';'.
def DECL(): # x : int = 5
    global lookahead
    global symbol_table
    global typ

    # non-terminal id
    id = lookahead
    match(id)

    # terminal ':'
    match(':')

    # non-terminal type so 'int' or 'real'
    typ = TYPE(lookahead)

    # terminal '='
    match('=')

    # non-terminal <expr> which uses id
    symbol_table[id] = EXPR()
    match(';')
    
# This method returns the type of the passed arguement 'typ' as a string. It's etiher
# real or int only for this language definition.
def TYPE(typ):
    if typ == 'real':
        match('real')
        return 'real'

    elif typ == 'int':
        match('int')
        return 'int'

    else:
        print('Error')
        exit()

# This method sets v by calling TERM(), and while the lookahead is either + or -
# it will match the + or - and then depending on the matched operand, add or subtract
# the next TERM() from the current value of v.
def EXPR():
    global lookahead
    v = TERM()
    while lookahead == '+' or lookahead == '-':
        if lookahead == '+':
            match('+')
            v += TERM()
        else:
            match('-')
            v -= TERM()
    return v
        
# This method sets v to FACTOR() and while the lookahead is either * or /
# it sets the symbol to the lookahead, and depending on the vlaue of symbol,
# it will either set v to v*FACTOR() or v/FACTOR(). Finally it returns v.
def TERM():
    #match(lookahead)
    v = FACTOR()
    while lookahead == '*' or lookahead == '/':
        symbol = lookahead
        match(lookahead)
        if symbol == '*':
            v *= FACTOR()
        else:
            symbol /= FACTOR()
    return v
    
# FACTOR function sets v to BASE() and if the lookahead is '^' it will match '^' and 
# then set v to v raised to the power of FACTOR(). Finally, it returns v.
def FACTOR():
    v = BASE()
    if lookahead == '^':
        match('^')
        v = v ** FACTOR()
    else: pass
    return v
        

# The BASE function will recursively call expr or type until an id from the symbol table or
# a valid int/real number is given. Like shown below:
# <base> ::= ( <expr> ) | id | number | <type> ( id )
def BASE():
    #v = 0
    # ( <expr> )
    if lookahead == '(':
        match('(')
        v = EXPR()
        match(v)
        match(')')

    # number -- real | int
    elif lookahead[0].isdigit and '.' in lookahead:
        v = float(lookahead)
          
    elif lookahead[0].isdigit():
        v = int(lookahead)
    
    # # <type> id
    elif lookahead == "int":
            TYPE()
            match('(')
            v = int(lookahead)
            match(')')
    
    elif lookahead == "real":
            typ = TYPE(lookahead)
            match('(')

            v = int(BASE())
            
            match(')')
    
    # id
    elif lookahead[0].isalpha():
        if lookahead in symbol_table:
            v = symbol_table[lookahead] # gets the value from the id

    else:
        print('ERROR')
        exit()

    match(lookahead)
    return v


# this function reads an input file (sys.argv[1] must be given) it then puts 
# the input into an iterable list which the tiny compiler runs on
def main():
    global mitr
    global lookahead
    global symbol_table
    global result
    result = []

    symbol_table = {}

    # if a file argument isn't given, then return error
    if(len(sys.argv) == 1 or len(sys.argv) > 2):
        print('Error')
        exit()
    
    # open the file
    with open(sys.argv[1], 'r+') as f:

        # create a list from the file, then iterate over that list
        wlist = f.read().split()
        mitr = iter(wlist)
        lookahead = next(mitr)

        # start the program
        PROG()
        
        #print the result by taking the list into a string
        print('\n'.join(result))


main()
