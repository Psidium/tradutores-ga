import re

lookup_table = {}


def get_name_identifier(name):
    try:
        return lookup_table[name]
    except KeyError:
        new_id = len(lookup_table) + 1
        lookup_table[name] = new_id
        return new_id


def compute_arithmetic_lexeme(lexeme):
    match = re.match('^([-+])?(.+?)$', lexeme)
    unary_operator = match.group(1)
    detached_lexeme = match.group(2)
    token_identifier = 'num' if re.search('\d+(?:\.\d+)?', detached_lexeme) else 'id'
    token = Token(token_identifier, detached_lexeme)

    if unary_operator:
        return [Token('unary_op', unary_operator), token]
    else:
        return [token]


class Token:
    def __init__(self, token, lexeme):
        self.token = token
        self.lexeme = lexeme

    def __str__(self):
        lexeme = get_name_identifier(self.lexeme) if self.token == 'id' else self.lexeme
        return '[' + self.token + ', ' + lexeme.__str__() + ']'

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

    def compute_arithmetic_expression(self):
        expression = re.compile('\s*(?:([-+*/])\s*((?:[-+])?(?:\d+(?:\.\d+)?|\w(?:(?:\w|\d)+)?))|((?:[-+])?(?:\d+(?:\.\d+)?|\w(?:(?:\w|\d)+)?)))\s*') # Error here: accepts other mixed expressions
        matches = expression.findall(self.right_side)
        tokens = []

        if len(matches) == 0:
            raise Exception('Invalid attribution expression for type "' + self.type + '": ' + self.right_side)

        for (operator, number, numberOnly) in matches:
            if numberOnly:
                tokens += compute_arithmetic_lexeme(numberOnly)
            else:
                tokens.append(Token('arith_op', operator))
                tokens += compute_arithmetic_lexeme(number)

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
            return self.compute_arithmetic_expression()
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


class FlowExpression:
    '''A Flow Expression is an `if` (followed or not by an else) or `while`'''
    def __init__(self, tokens):
        self.flow_start = tokens.group(1)
        self.comparison = ComparisonExpression(tokens.group(2))
        try:
            self.block = tokens.group(3)
            self.flow_else = tokens.group(4)
            self.else_block = tokens.group(5)
        except IndexError:
            pass

    def get_tokens(self):
        import tradutor_lexico
        tokens = [ Token('reserved_word', self.flow_start) ] + self.comparison.get_tokens()
        try:
            import pdb
            pdb.set_trace()
            tokens += tradutor_lexico.generate_tokens(self.block)
            tokens.append(Token('reserved_word', self.flow_else))
            tokens += tradutor_lexico.generate_tokens(self.else_block)
        except AttributeError:
            pass
        except TypeError:
            pass
        return tokens

class ComparisonExpression:
    def __init__(self, tokens):
        self.tokens = tokens

    def get_tokens(self):
        return []
