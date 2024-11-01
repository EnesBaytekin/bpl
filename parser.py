#!/bin/bash
from tokenizer import Token

class Node:
    def __init__(self, type, *children):
        self.type = type
        self.children = children
    def get_tree(self):
        return {
            "type": self.type,
            "children": [
                child.get_tree()
                if isinstance(child, Node)
                else
                {"type": child.type, "value": child.value}
                for child in self.children
            ]
        }

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
            checkpoint2 = self.index
            ENDL = self.match("ENDL")
            if ENDL is not None:
                statements = self.parse_statements()
                if statements is not None:
                    return Node("statements", statement, ENDL, statements)
            self.index = checkpoint2
            return Node("statements", statement)
        self.index = checkpoint
        ENDL = self.match("ENDL")
        if ENDL is not None:
            statements = self.parse_statements()
            if statements is not None:
                return Node("statements", ENDL, statements)
        self.index = checkpoint
        return Node("statements")
    def parse_statement(self):
        checkpoint = self.index
        OP_CURLY = self.match("{")
        if OP_CURLY is not None:
            statements = self.parse_statements()
            if statements is not None:
                CL_CURLY = self.match("}")
                if CL_CURLY is not None:
                    return Node("statement", OP_CURLY, statements, CL_CURLY)
        self.index = checkpoint
        assignment = self.parse_assignment()
        if assignment is not None:
            return Node("statement", assignment)
        self.index = checkpoint
        expression = self.parse_expression()
        if expression is not None:
            return Node("statement", expression)
        self.index = checkpoint
        DEL = self.match("DEL")
        if DEL is not None:
            VAR = self.match("VAR")
            if VAR is not None:
                OP_SQUARE = self.match("[")
                if OP_SQUARE is not None:
                    expression = self.parse_expression()
                    if expression is not None:
                        CL_SQUARE = self.match("]")
                        if CL_SQUARE is not None:
                            return Node("statement", DEL, VAR, OP_SQUARE, expression, CL_SQUARE)
        self.index = checkpoint
        function_definition = self.parse_function_definition()
        if function_definition is not None:
            return Node("statement", function_definition)
        self.index = checkpoint
        RETURN = self.match("RETURN")
        if RETURN is not None:
            expression = self.parse_expression()
            if expression is not None:
                return Node("statement", RETURN, expression)
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
                return Node("expression", addition, expression_)
        self.index = checkpoint
    def parse_assignment(self):
        checkpoint = self.index
        left_side = self.parse_left_side()
        if left_side is not None:
            checkpoint2 = self.index
            EQ = self.match("=")
            if EQ is not None:
                expression = self.parse_expression()
                if expression is not None:
                    return Node("assignment", left_side, EQ, expression)
            self.index = checkpoint2
            PLUS = self.match("+")
            if PLUS is not None:
                EQ = self.match("=")
                if EQ is not None:
                    expression = self.parse_expression()
                    if expression is not None:
                        return Node("assignment", left_side, PLUS, EQ, expression)
            self.index = checkpoint2
            MINUS = self.match("-")
            if MINUS is not None:
                EQ = self.match("=")
                if EQ is not None:
                    expression = self.parse_expression()
                    if expression is not None:
                        return Node("assignment", left_side, MINUS, EQ, expression)
            self.index = checkpoint2
            STAR = self.match("*")
            if STAR is not None:
                EQ = self.match("=")
                if EQ is not None:
                    expression = self.parse_expression()
                    if expression is not None:
                        return Node("assignment", left_side, STAR, EQ, expression)
            self.index = checkpoint2
            SLASH = self.match("/")
            if SLASH is not None:
                EQ = self.match("=")
                if EQ is not None:
                    expression = self.parse_expression()
                    if expression is not None:
                        return Node("assignment", left_side, SLASH, EQ, expression)
        self.index = checkpoint
    def parse_function_definition(self):
        checkpoint = self.index
        FUNC = self.match("FUNC")
        if FUNC is not None:
            VAR = self.match("VAR")
            if VAR is not None:
                OP_BRACKET = self.match("(")
                if OP_BRACKET is not None:
                    params = self.parse_params()
                    if params is not None:
                        CL_BRACKET = self.match(")")
                        if CL_BRACKET is not None:
                            OP_CURLY = self.match("{")
                            if OP_CURLY is not None:
                                statements = self.parse_statements()
                                if statements is not None:
                                    CL_CURLY = self.match("}")
                                    if CL_CURLY is not None:
                                        return Node("function_definition", FUNC, VAR, OP_BRACKET, params, CL_BRACKET, OP_CURLY, statements, CL_CURLY)
        self.index = checkpoint
    def parse_if_statement(self):
        checkpoint = self.index
        IF = self.match("IF")
        if IF is not None:
            expression = self.parse_expression()
            if expression is not None:
                OP_CURLY = self.match("{")
                if OP_CURLY is not None:
                    statements = self.parse_statements()
                    if statements is not None:
                        CL_CURLY = self.match("}")
                        if CL_CURLY is not None:
                            elif_statement = self.parse_elif_statement()
                            if elif_statement is not None:
                                return Node("if_statement", IF, expression, OP_CURLY, statements, CL_CURLY, elif_statement)
        self.index = checkpoint
    def parse_for_loop(self):
        checkpoint = self.index
        FOR = self.match("FOR")
        if FOR is not None:
            VAR = self.match("VAR")
            if VAR is not None:
                IN = self.match("IN")
                if IN is not None:
                    iterable = self.parse_iterable()
                    if iterable is not None:
                        OP_CURLY = self.match("{")
                        if OP_CURLY is not None:
                            statements = self.parse_statements()
                            if statements is not None:
                                CL_CURLY = self.match("}")
                                if CL_CURLY is not None:
                                    return Node("for_loop", FOR, VAR, IN, iterable, OP_CURLY, statements, CL_CURLY)
        self.index = checkpoint
    def parse_while_loop(self):
        checkpoint = self.index
        WHILE = self.match("WHILE")
        if WHILE is not None:
            expression = self.parse_expression()
            if expression is not None:
                OP_CURLY = self.match("{")
                if OP_CURLY is not None:
                    statements = self.parse_statements()
                    if statements is not None:
                        CL_CURLY = self.match("}")
                        if CL_CURLY is not None:
                            return Node("while_loop", WHILE, expression, OP_CURLY, statements, CL_CURLY)
        self.index = checkpoint
    def parse_addition(self):
        checkpoint = self.index
        term = self.parse_term()
        if term is not None:
            addition_ = self.parse_addition_()
            if addition_ is not None:
                return Node("addition", term, addition_)
        self.index = checkpoint
    def parse_expression_(self):
        checkpoint = self.index
        EQ1 = self.match("=")
        if EQ1 is not None:
            EQ2 = self.match("=")
            if EQ2 is not None:
                addition = self.parse_addition()
                if addition is not None:
                    return Node("expression_", EQ1, EQ2, addition)
        self.index = checkpoint
        EX = self.match("!")
        if EX is not None:
            EQ = self.match("=")
            if EQ is not None:
                addition = self.parse_addition()
                if addition is not None:
                    return Node("expression_", EX, EQ, addition)
        self.index = checkpoint
        LT = self.match("<")
        if LT is not None:
            checkpoint2 = self.index
            EQ = self.match("=")
            if EQ is not None:
                addition = self.parse_addition()
                if addition is not None:
                    return Node("expression_", LT, EQ, addition)
            self.index = checkpoint2
            addition = self.parse_addition()
            if addition is not None:
                return Node("expression_", LT, addition)
        self.index = checkpoint
        GT = self.match(">")
        if GT is not None:
            checkpoint2 = self.index
            EQ = self.match("=")
            if EQ is not None:
                addition = self.parse_addition()
                if addition is not None:
                    return Node("expression_", GT, EQ, addition)
            self.index = checkpoint2
            addition = self.parse_addition()
            if addition is not None:
                return Node("expression_", GT, addition)
        self.index = checkpoint
        return Node("expression_")
    def parse_left_side(self):
        checkpoint = self.index
        VAR = self.match("VAR")
        if VAR is not None:
            checkpoint2 = self.index
            OP_SQUARE = self.match("[")
            if OP_SQUARE is not None:
                expression = self.parse_expression()
                if expression is not None:
                    CL_SQUARE = self.match("]")
                    if CL_SQUARE is not None:
                        return Node("left_side", VAR, OP_SQUARE, expression, CL_SQUARE)
            self.index = checkpoint2
            return Node("left_side", VAR)
        self.index = checkpoint
    def parse_params(self):
        checkpoint = self.index
        VAR = self.match("VAR")
        if VAR is not None:
            params_ = self.parse_params_()
            if params_ is not None:
                return Node("params", VAR, params_)
        self.index = checkpoint
        return Node("params")
    def parse_elif_statement(self):
        checkpoint = self.index
        ELIF = self.match("ELIF")
        if ELIF is not None:
            expression = self.parse_expression()
            if expression is not None:
                OP_CURLY = self.match("{")
                if OP_CURLY is not None:
                    statements = self.parse_statements()
                    if statements is not None:
                        CL_CURLY = self.match("}")
                        if CL_CURLY is not None:
                            elif_statement = self.parse_elif_statement()
                            if elif_statement is not None:
                                return Node("elif_statement", ELIF, expression, OP_CURLY, statements, CL_CURLY, elif_statement)
        self.index = checkpoint
        else_statement = self.parse_else_statement()
        if else_statement is not None:
            return Node("elif_statement", else_statement)
        self.index = checkpoint
        return Node("elif_statement")
    def parse_iterable(self):
        checkpoint = self.index
        STR = self.match("STR")
        if STR is not None:
            return Node("iterable", STR)
        self.index = checkpoint
        list = self.parse_list()
        if list is not None:
            return Node("iterable", list)
        self.index = checkpoint
    def parse_term(self):
        checkpoint = self.index
        factor = self.parse_factor()
        if factor is not None:
            term_ = self.parse_term_()
            if term_ is not None:
                return Node("term", factor, term_)
        self.index = checkpoint
    def parse_addition_(self):
        checkpoint = self.index
        PLUS = self.match("+")
        if PLUS is not None:
            term = self.parse_term()
            if term is not None:
                addition_ = self.parse_addition_()
                if addition_ is not None:
                    return Node("addition_", PLUS, term, addition_)
        self.index = checkpoint
        MINUS = self.match("-")
        if MINUS is not None:
            term = self.parse_term()
            if term is not None:
                addition_ = self.parse_addition_()
                if addition_ is not None:
                    return Node("addition_", MINUS, term, addition_)
        self.index = checkpoint
        return Node("addition_")
    def parse_params_(self):
        checkpoint = self.index
        COMMA = self.match(",")
        if COMMA is not None:
            VAR = self.match("VAR")
            if VAR is not None:
                params_ = self.parse_params_()
                if params_ is not None:
                    return Node("params_", COMMA, VAR, params_)
        self.index = checkpoint
        return Node("params_")
    def parse_else_statement(self):
        checkpoint = self.index
        ELSE = self.match("ELSE")
        if ELSE is not None:
            OP_CURLY = self.match("{")
            if OP_CURLY is not None:
                statements = self.parse_statements()
                if statements is not None:
                    CL_CURLY = self.match("}")
                    if CL_CURLY is not None:
                        return Node("else_statement", ELSE, OP_CURLY, statements, CL_CURLY)
        self.index = checkpoint
    def parse_list(self):
        checkpoint = self.index
        OP_SQUARE = self.match("[")
        if OP_SQUARE is not None:
            items = self.parse_items()
            if items is not None:
                CL_SQUARE = self.match("]")
                if CL_SQUARE is not None:
                    return Node("list", OP_SQUARE, items, CL_SQUARE)
        self.index = checkpoint
    def parse_factor(self):
        checkpoint = self.index
        OP_BRACKET = self.match("(")
        if OP_BRACKET is not None:
            expression = self.parse_expression()
            if expression is not None:
                CL_BRACKET = self.match(")")
                if CL_BRACKET is not None:
                    return Node("factor", OP_BRACKET, expression, CL_BRACKET)
        self.index = checkpoint
        value = self.parse_value()
        if value is not None:
            return Node("factor", value)
        self.index = checkpoint
    def parse_term_(self):
        checkpoint = self.index
        STAR = self.match("*")
        if STAR is not None:
            factor = self.parse_factor()
            if factor is not None:
                term_ = self.parse_term_()
                if term_ is not None:
                    return Node("term_", STAR, factor, term_)
        self.index = checkpoint
        SLASH = self.match("/")
        if SLASH is not None:
            factor = self.parse_factor()
            if factor is not None:
                term_ = self.parse_term_()
                if term_ is not None:
                    return Node("term_", SLASH, factor, term_)
        self.index = checkpoint
        return Node("term_")
    def parse_items(self):
        checkpoint = self.index
        expression = self.parse_expression()
        if expression is not None:
            items_ = self.parse_items_()
            if items_ is not None:
                return Node("items", expression, items_)
        self.index = checkpoint
        return Node("items")
    def parse_value(self):
        checkpoint = self.index
        STR = self.match("STR")
        if STR is not None:
            return Node("value", STR)
        self.index = checkpoint
        INT = self.match("INT")
        if INT is not None:
            return Node("value", INT)
        self.index = checkpoint
        FLOAT = self.match("FLOAT")
        if FLOAT is not None:
            return Node("value", FLOAT)
        self.index = checkpoint
        list = self.parse_list()
        if list is not None:
            return Node("value", list)
        self.index = checkpoint
        function_call = self.parse_function_call()
        if function_call is not None:
            return Node("value", function_call)
        self.index = checkpoint
        VAR = self.match("VAR")
        if VAR is not None:
            checkpoint2 = self.index
            OP_SQUARE = self.match("[")
            if OP_SQUARE is not None:
                expression = self.parse_expression()
                if expression is not None:
                    CL_SQUARE = self.match("]")
                    if CL_SQUARE is not None:
                        return Node("value", VAR, OP_SQUARE, expression, CL_SQUARE)
            self.index = checkpoint2
            return Node("value", VAR)
        self.index = checkpoint
    def parse_items_(self):
        checkpoint = self.index
        COMMA = self.match(",")
        if COMMA is not None:
            expression = self.parse_expression()
            if expression is not None:
                items_ = self.parse_items_()
                if items_ is not None:
                    return Node("items_", COMMA, expression, items_)
        self.index = checkpoint
        return Node("items_")
    def parse_function_call(self):
        checkpoint = self.index
        VAR = self.match("VAR")
        if VAR is not None:
            if self.match("(") is not None:
                items = self.parse_items()
                if items is not None:
                    if self.match(")") is not None:
                        return Node("function_call", VAR, items)
        self.index = checkpoint
