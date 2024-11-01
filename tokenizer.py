#!/bin/python

class Token:
    def __init__(self, type: str, value: str=""):
        self.type = type
        self.value = value
    def __repr__(self):
        type = repr(self.type) if len(self.type) == 1 else self.type
        if self.value == "":
            return f"<{type}>"
        else:
            return f"<{type} '{self.value}'>"

def tokenize(source: str):
    tokens = []
    state = "idle"
    value = ""
    index = 0
    while index < len(source):
        c = source[index]
        if state == "idle":
            if c in ["'", '"']:
                value = c
                state = "string"
            elif c.isdigit() or c == "-":
                value = c
                state = "number"
            elif c.isalpha() or c == "_":
                value = c
                state = "word"
            elif c in list("[](){}=+-/*,<>!"):
                tokens.append(Token(c))
            elif c == "\n":
                tokens.append(Token("ENDL"))
            elif c == "#":
                state = "comment"
        elif state == "string":
            if c == value[0]:
                state = "idle"
                tokens.append(Token("STR", value[1:]))
            else:
                value += c
        elif state == "number":
            if value == "0" and c == "x":
                value = ""
                state = "hex"
            elif value == "0" and c == "b":
                value = ""
                state = "bin"
            elif c == ".":
                value += c
                state = "float"
            elif c.isdigit():
                value += c
            else:
                tokens.append(Token("INT", int(value)))
                state = "idle"
                index -= 1
        elif state == "hex":
            if c in "0123456789abcdefABCDEF":
                value += c
            else:
                tokens.append(Token("INT", int(value, 16)))
                state = "idle"
                index -= 1
        elif state == "bin":
            if c in "01":
                value += c
            else:
                tokens.append(Token("INT", int(value, 2)))
                state = "idle"
                index -= 1
        elif state == "float":
            if value == "-.":
                print("Invalid syntax: -.")
                exit(0)
            elif c.isdigit():
                value += c
            else:
                tokens.append(Token("FLOAT", float(value)))
                state = "idle"
                index -= 1
        elif state == "word":
            if c.isalnum() or c == "_":
                value += c
            else:
                if value in ["if", "elif", "else", "del", "func", "return", "for", "in", "while"]:
                    tokens.append(Token(value.upper()))
                else:
                    tokens.append(Token("VAR", value))
                state = "idle"
                index -= 1
        elif state == "comment":
            if c == "\n":
                state = "idle"
                index -= 1
        index += 1
    return tokens
