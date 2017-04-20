#! /bin/python

import sys
import re


class AttributionExpression:
    def __init__(self, tokens):
        self.type = tokens.group(1)
        self.name = tokens.group(2)
        self.right_side = tokens.group(3)

    def get_tokens(self):
        return ['[reserved_word, ' + self.type + ']', '[id, ' + self.name + ']',
                '[equal_op, =]'] + self.compute_right_side()

    def compute_right_side(self):
        expression = re.compile('(?:([-+*/])\s*((?:[-+])?\d+(?:\.\d+)?)|((?:[-+])?\d+(?:\.\d+)?))')
        matches = expression.findall(self.right_side)
        tokens = []

        for (operator, number, numberOnly) in matches:
            if numberOnly:
                tokens.append('[num, ' + numberOnly + ']')
            else:
                tokens.append('[arith_op, ' + operator + ']')
                tokens.append('[num, ' + number + ']')

        return tokens


class DefinitionExpression:
    def __init__(self, tokens):
        self.type = tokens.group(1)
        self.name = tokens.group(2)

    def get_tokens(self):
        return ['[reserved_word, ' + self.type + ']', '[id, ' + self.name + ']']


# Script
expressions = [{
    'regex': re.compile('(int|float)\s+(\w(?:(?:\w|\d)+)?)\s*=\s*((?:[-+])?\d+(?:\.\d+)?\s*(?:(?:[-+*/]\s*(?:(?:[-+])?\d+(?:\.\d+)?))+)?)\s*;'),
    'tokenizer': AttributionExpression
}, {
    'regex': re.compile('(int|float)\s+(\w(?:(\w|\d)+)?)\s*;'),
    'tokenizer': DefinitionExpression
}]


def normalize_spaces(source):
    return re.sub(r'(?!\n)\s+', ' ', source)  # We don't need to consider strings


def remove_comments(source):
    return re.sub(r'(//.+?$|/\*(.|\s)+?\*/)', '', source)


def remove_empty_lines(split_source):
    return [l for l in split_source if l]


def clean_source(source):
    return normalize_spaces(remove_comments(source))


def read_program_from_file(path):
    f = open(path)
    source = f.read()
    return remove_empty_lines(clean_source(source).split('\n'))


def get_tokenizer(program_line):
    for expression in expressions:
        tokens = expression['regex'].match(program_line)
        if tokens is not None:
            return expression['tokenizer'](tokens)

    return None


def print_tokens(tokens):
    print(' '.join(tokens))


if len(sys.argv) < 2:
    print('Wrong number of arguments passed.')
    sys.exit()

program_lines = read_program_from_file(sys.argv[1])

for line in program_lines:
    tokenizer = get_tokenizer(line)
    if tokenizer is not None:
        print_tokens(tokenizer.get_tokens())
    else:
        print('Failed to compute expression: "' + line + '"')
