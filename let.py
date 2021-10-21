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
# terminal characters are space delimited and the input file name is given from cmd.

# #!/usr/bin/python3
# chmod +x let.py

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
        print('Syntax Error')
        exit()

def PROG():
    global lookahead
    symbol_table = {} #clear symbol_table at end of program
    LET_IN_END()
    while lookahead == 'let':
        symbol_table = {} #clear symbol_table at end of program
        LET_IN_END()
    

def LET_IN_END():
    global lookahead
    global symbol_table
    match('let')
    DECL_LIST()
    match('in')
    typ = TYPE()
    match('(')
    value = EXPR()
    match(')')
    ######################################################################print(value)
    match('end')
    match(';')



def DECL_LIST():
    global lookahead
    DECL()
    while lookahead == '':
        DECL()


    

    
def DECL():
    global lookahead
    global symbol_table
    id = lookahead
    match(lookahead)
    match(':')
    typ = TYPE()
    v = EXPR()
    match(';')
    symbol_table[id] = v
    
  
    
def TYPE(v):
    if isinstance(v, int):
        return "int" 
    elif isinstance(v, real):
        return "real"
    else:
        print("Type Error")
        exit()
    
    

def EXPR():
    v = TERM(expr_type)
    while lookahead == '+' or lookahead == '-':
        if lookahead == '+':
            match('+')
            v += TERM(expr_type)
        else:
            match('-')
            v -= TERM(expr_type)
    return v
        
        
def TERM():
    FACTOR()
    while lookahead == '*' or lookahead == '/':
        FACTOR()
    
    
def FACTOR():
    BASE()
    if lookahead == '^':
        match('^')
        FACTOR()
    else: pass
        

# type checking must be done to ensure lookahead is expr_type
def BASE():
    #first character of lookahead
    if lookahead == '(':
        match('(')
        EXPR()
        match(')')

    elif lookahead[0].isdigit():
        v = int(lookahead)

    elif '.' in lookahead:
        v = float(lookahead)

    elif lookahead == "int" or lookahead == "real":
            TYPE()
            match('(')
            id = lookahead
            match(')')
        
    elif lookahead[0].isalpha():
        if lookahead in symbol_table:
            v = symbol_table[lookahead]
            if typ == 'int':
                if isinstance(v, int) == False:
                    print('Error')
                    exit()
                else: return v
            elif expr_type == 'real':
                if(isinstance(v, real) == False):
                    print('Error')
                    exit()
                else: return v
            else: print("Error") # If the expr_type is not int or real            


                    
    
    
    
    
    match(lookahead)
    return v
    # do not use eval() function!!









    
    
    
    

def main():
    global mitr
    global lookahead
    global symbol_table
    symbol_table = {}

    # if a file argument isn't given, then return error
    if(len(sys.argv) == 1):
        print('Syntax Error: no file given')
        exit()
    
    # open the file
    with open(sys.argv[1], 'r+') as f:

        # create a list, then iterate over that list
        wlist = f.read().split()
        mitr = iter(wlist)
        lookahead = next(mitr)
        PROG()
        if(lookahead == ''):
            print('pass')
        else:
            print('Syntax Error')

main()
