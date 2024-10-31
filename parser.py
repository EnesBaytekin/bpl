#!/bin/bash
from tokenizer import Token

class Node:
    def __init__(self, type, *children):
        self.type = type
        self.children = children
    def get_tree(self):
        return {"type": self.type, "children": [child.get_tree() for child in self.children]}

class Parser:
    def __init__(self, tokens: list[Token]):
        self.tokens = tokens
        self.index = 0
    def match(self, token_type):
        if self.index >= len(self.tokens):
            return
        token = self.tokens[self.index]
        if token_type == token.type:
            self.index += 1
            return token
    def parse(self):
        return self.parse_program()
    def parse_program(self):
        statements = self.parse_statements()
        if statements is not None:
            return Node("program", statements)
    def parse_statements(self):
        checkpoint = self.index
        statement = self.parse_statement()
        if statement is not None:
            if self.match("ENDL") is not None:
                statements = self.parse_statements()
                if statements is not None:
                    return Node("statements", statement, statements)
            else:
                return Node("statements", statement)
        self.index = checkpoint
        if self.match("ENDL") is not None:
            statements = self.parse_statements()
            if statements is not None:
                return Node("statements", statements)
        self.index = checkpoint
        return Node("statements")
    def parse_statement(self):
        
        
