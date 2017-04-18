#! /bin/python

import sys
import re

class AttributionExpression:
    def __init__(self, matcher):
        self.type = matcher[1];
        self.name = matcher[2];
        self.value = matcher[3];

    def get_tokens(self):
        return [
            "[reserved_word, " + self.type + "]",
            "[id, " + self.name + "]",
            "[Equal_Op,=]",
            "[value, " + self.value + "]",
        ]

class DefinitionExpression:
    def __init__(self, matcher):
        self.type = matcher[1];
        self.name = matcher[2];

    def get_tokens(self):
        return [
            "[reserved_word, " + self.type + "]",
            "[id, " + self.name + "]"
        ]

reserved_words = [ 'printf', 'int' ];
operators = {
    '=' : 'Equal_Operator'
}

attribution = re.compile('(int)\s(\w+)[\s|=]+(\d);')
definition = re.compile('(int)\s(\w+);')

def read_program_from_file(path):
    f = open(path)
    return f.read().split('\n')

def get_splitter(expression):
    result = attribution.match(expression)
    if (result != None):
        return AttributionExpression(result)
    result = definition.match(expression)
    if (result != None):
        return DefinitionExpression(expression)
    return None

if (len(sys.argv) < 2):
    print("Fuck you")
    sys.exit()

tokens = []
program_lines = read_program_from_file(sys.argv[1])
for line in program_lines:
    splitter = get_splitter(line)
    if splitter != None:
        print(splitter.get_tokens())
    else:
        print("Failed to compute expression: \"" + line + "\"")

