#!/bin/python

from sys import argv
from tokenizer import tokenize
from parser import Parser

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
    parser = Parser(tokens)
    parse_tree = parser.parse()
    tree_string = parse_tree.get_tree()
    from json import loads, dumps
    print(dumps(tree_string, indent=2))
    
if __name__ == "__main__":
    main()
