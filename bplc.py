#!/bin/python

from sys import argv
from tokenizer import tokenize
def show_help():
    print(
"""Usage:
    bplc <file>
""", end="")

def main():
    if len(argv) != 2:
        show_help()
        exit(0)
    try:
        with open(argv[1], "r") as file:
            data = file.read()
    except IOError:
        print("File could not be found.") 
        exit(0)
    tokens = tokenize(data)
    for token in tokens:
        print(token, end=" ")
        if token.type == "ENDL":
            print()
    
if __name__ == "__main__":
    main()
