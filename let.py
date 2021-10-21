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
# <let-in-end> ::= let <decl-list> in <type> ( <expr> ) end ;
# <decl-list> ::= <decl> { <decl> }
# <decl> ::= id : <type> = <expr> ;
# <type> ::= int | real
# <expr> ::= <term> { + <term> | - <term> }
# <term> ::= <factor> { * <factor> | / <factor> }
# <factor> ::= <base> ^ <factor> | <base>
# <base> ::= ( <expr> ) | id | number | <type> ( id )
# terminal characters are space delimited and the input file name is given from cmd.

import sys
# NEED TO IMPLEMENT:
# functions: TERM(expr_type) TYPE() FACTOR() DECLR_LIST()

def lexan():
    global mitr
    try:
        return next(mitr)
    except StopIteration:
        return ('')

def match(ch):
    global lookahead
    if(ch == lookahead):
        lookahead = lexan()
    else:
        print('Syntax Error')
        exit()

def PROG():
    global lookahead
    LET_IN_END()
    while (lookahead == 'let'):
        LET_IN_END()

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

    
    
def DECL_LIST():
    DECL()
    match('{')
    DECL()
    match('}')
    

    
def DECL():
    global lookahead
    global symbol_table
    id = lookahead
    match(lookahead)
    match(':')
    typ = TYPE()
    v = EXPR()
    symbol_table[id] = v
    
  
    
def TYPE():
    
    
    
def EXPR():
    v = TERM(expr_type)
    while (lookahead == '+' or lookahead == 'i'):
        if (lookahead == '+'):
            match('+')
            v += TERM(expr_type)
        else:
            match('-')
            v -= TERM(expr_type)
          
        
        
def TERM():
    
    
    
def FACTOR():
            


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
