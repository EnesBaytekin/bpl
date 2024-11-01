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
    debug(parse_tree)

def debug(parse_tree):
    tree_object = parse_tree.get_tree()
    from debug import create_tree_image
    create_tree_image(tree_object, "debug/tree")
    
if __name__ == "__main__":
    main()
