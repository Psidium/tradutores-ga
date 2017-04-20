import re


class Token:
    def __init__(self, token, lexeme):
        self.token = token
        self.lexeme = lexeme

    def __str__(self):
        return '[' + self.token + ', ' + self.lexeme + ']'

    def __repr__(self):
        return self.__str__()


class AttributionExpression:
    def __init__(self, tokens):
        self.type = tokens.group(1)
        self.name = tokens.group(2)
        self.right_side = tokens.group(3)

    def get_tokens(self):
        if not re.search('^(int|float|double|string|bool)$', self.type):
            raise Exception('Unknown type "' + self.type + '"')

        return [Token('reserved_word', self.type), Token('id', self.name), Token('equal_op', '=')] + self.compute_right_side_tokens()

    def compute_number_expression(self):
        expression = re.compile('\s*(?:([-+*/])\s*((?:[-+])?\d+(?:\.\d+)?)|((?:[-+])?\d+(?:\.\d+)?))\s*') # Error here: accepts other mixed expressions
        matches = expression.findall(self.right_side)
        tokens = []

        if len(matches) == 0:
            raise Exception('Invalid attribution expression for type "' + self.type + '": ' + self.right_side)

        for (operator, number, numberOnly) in matches:
            if numberOnly:
                tokens.append(Token('num', numberOnly))
            else:
                tokens.append(Token('arith_op', operator))
                tokens.append(Token('num', number))

        return tokens

    def compute_simple_expression(self, regex, token_identifier):
        match = regex.match(self.right_side)
        expression = match.group(1) if match is not None else None

        if expression:
            return [Token('reserved_word' if expression == 'null' else token_identifier, expression)]
        else:
            raise Exception('Invalid attribution expression for type "' + self.type + '": ' + self.right_side)

    def compute_string(self):
        return self.compute_simple_expression(re.compile('^\s*(".+?"|null)\s*$'), 'string_literal')

    def compute_boolean(self):
        return self.compute_simple_expression(re.compile('^\s*(true|false)\s*$'), 'reserved_word')

    def compute_right_side_tokens(self):
        if self.type == 'string':
            return self.compute_string()
        elif re.search('^(int|float|double)$', self.type):
            return self.compute_number_expression()
        elif self.type == 'bool':
            return self.compute_boolean()
        else:
            raise Exception('Unknown type "' + self.type + '"')


class DefinitionExpression:
    def __init__(self, tokens):
        self.type = tokens.group(1)
        self.name = tokens.group(2)

    def get_tokens(self):
        if not re.search('^(int|float|double|string|bool)$', self.type):
            raise Exception('Unknown type "' + self.type + '"')

        return [Token('reserved_word', self.type), Token('id', self.name)]


class IfExpression:
    def __init__(self, tokens):
        pass
