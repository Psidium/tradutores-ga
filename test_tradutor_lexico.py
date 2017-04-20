import unittest
import tradutor_lexico

class TestLexical(unittest.TestCase):
    def test_definition(self):
        tokens = tradutor_lexico.generate_tokens("int a;")
        self.assertEquals(len(tokens), 2)
        self.assertEquals(tokens[0].token, "reserved_word")
        self.assertEquals(tokens[0].lexeme, "int")
        self.assertEquals(tokens[1].token, "id")
        self.assertEquals(tokens[1].lexeme, "a")

    def test_definition_with_comments(self):
        tokens = tradutor_lexico.generate_tokens("int a; // 'a' is a terrible variable name")
        self.assertEquals(len(tokens), 2)
        self.assertEquals(tokens[0].token, "reserved_word")
        self.assertEquals(tokens[0].lexeme, "int")
        self.assertEquals(tokens[1].token, "id")
        self.assertEquals(tokens[1].lexeme, "a")


    def test_attribution(self):
        tokens = tradutor_lexico.generate_tokens("int a = 32;")
        self.assertEquals(len(tokens), 4)
        self.assertEquals(tokens[0].token, "reserved_word")
        self.assertEquals(tokens[0].lexeme, "int")
        self.assertEquals(tokens[1].token, "id")
        self.assertEquals(tokens[1].lexeme, "a")
        self.assertEquals(tokens[2].token, "equal_op")
        self.assertEquals(tokens[2].lexeme, "=")
        self.assertEquals(tokens[3].token, "num")
        self.assertEquals(tokens[3].lexeme, "32")


    def test_attribution_with_comments(self):
        tokens = tradutor_lexico.generate_tokens("int a = 32; //a again")
        self.assertEquals(len(tokens), 4)
        self.assertEquals(tokens[0].token, "reserved_word")
        self.assertEquals(tokens[0].lexeme, "int")
        self.assertEquals(tokens[1].token, "id")
        self.assertEquals(tokens[1].lexeme, "a")
        self.assertEquals(tokens[2].token, "equal_op")
        self.assertEquals(tokens[2].lexeme, "=")
        self.assertEquals(tokens[3].token, "num")
        self.assertEquals(tokens[3].lexeme, "32")

    def test_should_return_none_when_invalid_command(self):
        tokens = tradutor_lexico.generate_tokens("int = int")
        self.assertEquals(tokens, None)

if __name__ == "__main__":
    unittest.main()
