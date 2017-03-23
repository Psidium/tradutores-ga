#! /bin/python


reserved_words = ['printf', 'int' ];
out = []

def tokenizer(src):
    src = ' '.join(src.split())
    spaceless_program = src.split(' ')
    for word in spaceless_program:
        for i, reserved_word in enumerate(reserved_words):
            if reserved_word == word:
                out.push(('reserved_word', i))

