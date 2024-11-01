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
        self.index = checkpoint
    def parse_expression(self):
        checkpoint = self.index
        addition = self.parse_addition()
        if addition is not None:
            expression_ = self.parse_expression_()
            if expression_ is not None:
                return Node("addition", addition, expression_)
        self.index = checkpoint
    def parse_assignment(self):
        checkpoint = self.index
        left_side = self.parse_left_side()
        if left_side is not None:
            checkpoint2 = self.index
            if self.match("=") is not None:
                expression = self.parse_expression()
                if expression is not None:
                    return Node("assignment", left_side, expression)
            self.index = checkpoint2
            if self.match("+") is not None:
                if self.match("=") is not None:
                    expression = self.parse_expression()
                    if expression is not None:
                        return Node("assignment", left_side, expression)
            self.index = checkpoint2
            if self.match("-") is not None:
                if self.match("=") is not None:
                    expression = self.parse_expression()
                    if expression is not None:
                        return Node("assignment", left_side, expression)
            self.index = checkpoint2
            if self.match("*") is not None:
                if self.match("=") is not None:
                    expression = self.parse_expression()
                    if expression is not None:
                        return Node("assignment", left_side, expression)
            self.index = checkpoint2
            if self.match("/") is not None:
                if self.match("=") is not None:
                    expression = self.parse_expression()
                    if expression is not None:
                        return Node("assignment", left_side, expression)
        self.index = checkpoint
    def parse_function_definition(self):
        checkpoint = self.index
        if self.match("FUNC") is not None:
            VAR = self.match("VAR")
            if VAR is not None:
                if self.match("(") is not None:
                    params = self.parse_params()
                    if params is not None:
                        if self.match(")") is not None:
                            if self.match("{") is not None:
                                statements = self.parse_statements()
                                if statements is not None:
                                    if self.match("}") is not None:
                                        return Node("function_definition", VAR, params, statements)
        self.index = checkpoint
    def parse_if_statement(self):
        checkpoint = self.index
        if self.match("IF") is not None:
            expression = self.parse_expression()
            if expression is not None:
                if self.match("{") is not None:
                    statements = self.parse_statements()
                    if statements is not None:
                        if self.match("}") is not None:
                            elif_statement = self.parse_elif_statement()
                            if elif_statement is not None:
                                return Node("if_statement", expression, statements, elif_statement)
        self.index = checkpoint
    def parse_for_loop(self):
        checkpoint = self.index
        if self.match("FOR") is not None:
            VAR = self.match("VAR")
            if VAR is not None:
                if self.match("IN") is not None:
                    iterable = self.parse_iterable()
                    if iterable is not None:
                        if self.match("{") is not None:
                            statements = self.parse_statements()
                            if statements is not None:
                                if self.match("}") is not None:
                                    return Node("for_loop", VAR, iterable, statements)
        self.index = checkpoint
    def parse_while_loop(self):
        checkpoint = self.index
        if self.match("WHILE") is not None:
            expression = self.parse_expression()
            if expression is not None:
                if self.match("{") is not None:
                    statements = self.parse_statements()
                    if statements is not None:
                        if self.match("}") is not None:
                            return Node("while_loop", expression, statements)
        self.index = checkpoint
    def parse_addition(self):
        return Node("addition")
    def parse_expression_(self):
        return Node("expression_")
    def parse_left_side(self):
        return Node("left_side")
    def parse_params(self):
        return Node("params")
    def parse_elif_statement(self):
        return Node("elif_statement")
    def parse_parse_iterable(self):
        return Node("parse_iterable")
