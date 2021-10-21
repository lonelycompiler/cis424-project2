#!/bin/python3
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

# NEED TO IMPLEMENT:
# functions: TERM(expr_type) TYPE() FACTOR() DECLR_LIST()
# clear dict after matching ;
def lexan():
    global mitr
    try:
        return next(mitr)
    except StopIteration:
        return ''


def match(ch):
    global lookahead
    if(ch == lookahead):
        lookahead = lexan()
    else:
        print('Error')
        exit()

def PROG():
    global lookahead
    LET_IN_END()
    while lookahead == 'let':
        LET_IN_END()
    

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


def DECL_LIST():
    global lookahead
    DECL()
    while lookahead != 'in':
        DECL()


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
    

def FACTOR():
    v = BASE()
    if lookahead == '^':
        match('^')
        v = v ** FACTOR()
    else: pass
    return v
        

# type checking must be done to ensure lookahead is expr_type
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
            id = int(lookahead)
            match(')')
            v = id
    
    elif lookahead == "real":
            typ = TYPE(lookahead)
            match('(')

            if ( lookahead[0].isalpha()): 
                id = int(BASE())
            match(')')
            v = id
    
    # id
    elif lookahead[0].isalpha():
        if lookahead in symbol_table:
            v = symbol_table[lookahead] # gets the value from the id

    else:
        print('ERROR')
        exit()

    match(lookahead)
    return v


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

        # create a list, then iterate over that list
        wlist = f.read().split()
        mitr = iter(wlist)
        lookahead = next(mitr)
        PROG()
        
        #print the result by taking the list into a string
        print('\n'.join(result))

main()
