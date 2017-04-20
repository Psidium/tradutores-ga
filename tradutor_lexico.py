#! /bin/python

import sys
import re
import tokenizers

# Script
expressions = [{
    'regex': re.compile('(\w(?:(?:\w|\d)+)?)\s+(\w(?:(?:\w|\d)+)?)\s*=(.+?);'),
    'tokenizer': tokenizers.AttributionExpression
}, {
    'regex': re.compile('(\w(?:(?:\w|\d)+)?)\s+(\w(?:(\w|\d)+)?)\s*;'),
    'tokenizer': tokenizers.DefinitionExpression
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
    for token in tokens:
        print token,

    print


if len(sys.argv) < 2:
    print('Wrong number of arguments passed.')
    sys.exit()

program_lines = read_program_from_file(sys.argv[1])

for line in program_lines:
    tokenizer = get_tokenizer(line)

    if tokenizer is not None:
        try:
            print_tokens(tokenizer.get_tokens())
        except Exception as e:
            print(e.message)
    else:
        print('Failed to compute expression: "' + line + '"')
