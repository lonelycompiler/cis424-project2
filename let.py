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
import snoop
# NEED TO IMPLEMENT:
# functions: TERM(expr_type) TYPE() FACTOR() DECLR_LIST()
# clear dict after matching ;
def lexan():
    global mitr
    try:
        return next(mitr)
    except StopIteration:
        return ''

@snoop(watch='lookahead', depth=2)
def match(ch):
    global lookahead
    if(ch == lookahead):
        lookahead = lexan()
    else:
        print('Error')
        exit()

@snoop(watch='lookahead', depth=2)
def PROG():
    global lookahead
    symbol_table = {} #clear symbol_table at end of program
    LET_IN_END()
    while lookahead == 'let':
        symbol_table = {} #clear symbol_table at end of program
        LET_IN_END()
    

@snoop(watch='lookahead', depth=2)
def LET_IN_END():
    global lookahead
    global symbol_table
    match('let')
    DECL_LIST()
    match('in')

    typ = TYPE(lookahead)

    match('(')
    value = EXPR()
    match(')')
    ######################################################################print(value)
    match('end')
    match(';')



@snoop(watch='lookahead', depth=2)
def DECL_LIST():
    global lookahead
    DECL()
    while lookahead == '':
        DECL()


    

@snoop(watch='lookahead', depth=3)
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
    v = EXPR()
    match(';')
    symbol_table[id] = v
    
  
@snoop(watch='lookahead', depth=2)
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
    """
    try:
        if '.' in v:
            v = float(v)
            return 'real'
        else:
            try:
                v = int(v)
                return 'int'
            except:
                print('Error')
                exit()
    except:
        try:
            v = int(v)
            return 'int'
        except:
            print('Error')
            exit()
    """
    
    

def EXPR():
    global lookahead
    #print(lookahead)
    v = TERM()
    #print(v)
    while lookahead == '+' or lookahead == '-':
        if lookahead == '+':
            match('+')
            v += TERM()
        else:
            match('-')
            v -= TERM()
    return v
        
        
def TERM():
    match(lookahead)
    FACTOR()
    while lookahead == '*' or lookahead == '/':
        match(lookahead)
        FACTOR()
    
    
@snoop(watch='lookahead', depth=2)
def FACTOR():
    #print(lookahead)
    BASE()
    if lookahead == '^':
        match('^')
        FACTOR()
    else: pass
        

# type checking must be done to ensure lookahead is expr_type

@snoop(watch='lookahead', depth=2)
def BASE():
    # ( <expr> )
    if lookahead == '(':
        match('(')
        EXPR()
        match(')')
    
    # id
    elif lookahead[0].isalpha():
        if lookahead in symbol_table:
            v = symbol_table[lookahead] # gets the value from the id
            
            """
            if typ == 'int':
                if isinstance(v, int) == False:
                    print('Error')
                    exit()
                else: return v
            elif typ == 'real':
                if(isinstance(v, float) == False):
                    print('Error')
                    exit()
                else: return v
            else:
                print("Error") # If the expr_type is not int or real
                exit()
            """

    # number -- real
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
            TYPE()
            match('(')
            id = int(lookahead)
            match(')')
            v = id

    match(lookahead)
    return v










    
    
    
    

@snoop(watch='lookahead', depth=2)
def main():
    global mitr
    global lookahead
    global symbol_table
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
        if(lookahead == ''):
            print('pass')
        else:
            print('hi')
            print('Error')

main()
