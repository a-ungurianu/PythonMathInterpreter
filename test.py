from interpret import *
import unittest

class TestNumberParsing(unittest.TestCase):

    def setUp(self):
        self.parser = Parser()

    def test_parsePositiveInteger(self):
        numbers = ["1","1000","3123123213","123","0"]

        for number in numbers:
            numberNode = self.parser.parse(number)
            self.assertEqual(numberNode.eval(),int(number))

    def test_parseNegativeInteger(self):
        numbers = ["-1","-1000","-1232132132131","-123","-0"]

        for number in numbers:
            numberNode = self.parser.parse(number)
            self.assertEqual(numberNode.eval(),int(number))

    def test_parsePositiveFloat(self):
        numbers = ["0.0","1.3333333","1231.13","2332.232","33333.3",".33"]

        for number in numbers:
            numberNode = self.parser.parse(number)
            self.assertEqual(numberNode.eval(), float(number))

    def test_parseNegativeFloat(self):
        numbers = ["-0.0","-1.223232","-13123.23","-32432423423423.0","-34324.33333333"]

        for number in numbers:
            numberNode = self.parser.parse(number)
            self.assertEqual(numberNode.eval(),float(number))

    def test_failToParseNumbers(self):
        bad_numbers = ["0.0.0","23a","a23","123-","3...3"]

        for number in bad_numbers:
            with self.assertRaises(ParseError):
                numberNode = self.parser.parse(number)

if __name__ == "__main__":
    unittest.main()