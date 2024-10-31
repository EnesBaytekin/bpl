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
        checkpoint = self.index
        if self.match("{") is not None:
            statements = self.parse_statements()
            if statements is not None:
                if self.match("}") is not None:
                    return Node("statement", statements)
        self.index = checkpoint
        expression = self.parse_expression()
        if expression is not None:
            return Node("statement", expression)
        self.index = checkpoint
        assignment = self.parse_assignment()
        if assignment is not None:
            return Node("statement", assignment)
        self.index = checkpoint
        if self.match("DEL") is not None:
            VAR = self.match("VAR")
            if VAR is not None:
                if self.match("[") is not None:
                    expression = self.parse_expression()
                    if expression is not None:
                        if self.match("]") is not None:
                            return Node("statement", VAR, expression)
        self.index = checkpoint
        function_definition = self.parse_function_definition()
        if function_definition is not None:
            return Node("statement", function_definition)
        self.index = checkpoint
        if_statement = self.parse_if_statement()
        if if_statement is not None:
            return Node("statement", if_statement)
        self.index = checkpoint
        for_loop = self.parse_for_loop()
        if for_loop is not None:
            return Node("statement", for_loop)
        self.index = checkpoint
        while_loop = self.parse_while_loop()
        if while_loop is not None:
            return Node("statement", while_loop)
    def parse_expression(self):
    def parse_assignment(self):
    def parse_function_definition(self):
    def parse_if_statement(self):
    def parse_for_loop(self):
    def parse_while_loop(self):
        
