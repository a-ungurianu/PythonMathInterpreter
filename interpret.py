import argparse, os

import string

class ParseError(Exception):
	def __init__(self, value):
		self.value = value
	def __str__(self):
		return repr(self.value)

class ASTNode(object):

	def __init__(self):
		pass

	def eval():
		raise NotImplementedError

class BinaryExpression(ASTNode):

	def __init__(self, first_term, second_term, operation):
		self.first_term = first_term
		self.second_term = second_term
		self.operation = operation

	def eval(self):
		return self.operation(self.first_term.eval(), self.second_term.eval())

class Factor(ASTNode):
	def __init__(self,child,negate=False):
		self.negate = negate
		self.child = child

	def eval(self):
		return self.child.eval() * (-1 if self.negate else 1)

class Number(ASTNode):
	def __init__(self,number):
		self.number = number

	def eval(self):
		return self.number

class Identifier(ASTNode):
	def __init__(self, identifier):
		self.identifier = identifier
	
	def eval(self,context):
		return context.variables[Identifier]

class Assignment(ASTNode):
	def __init__(self, identifier, value):
		self.identifier = identifier
		self.value = value
	
	def eval(self,context):
		context.variables[self.identifier] = self.value.eval()

class Parser:

	op_dict = { "+": lambda a, b: a + b,
				"-": lambda a, b: a - b,
				"*": lambda a, b: a * b,
				"/": lambda a, b: a / b,
				"%": lambda a, b: a % b}

	non_zero_digits = "123456789"
	digits = "0" + non_zero_digits

	def __init__(self):
		self.stream = ""

	def parse(self, exp_string):
		self.stream_index = 0
		self.stream = exp_string + "$"

		ast = self._expression()
		if self.stream[self.stream_index] != "$":
			raise ParseError("The line wasn't just an expression")

		return ast

	def _get_current_char(self):
		return self.stream[self.stream_index]

	def _assignment(self):
		identif = self._identifier()
		
		self._whitespace()

		if self._get_current_char() != "=":
			raise ParseError("Expected equal sign in assigment operation")
		else:
			self.stream_index += 1

		self._whitespace()
		value = self._expression()

		return Assignment(identif, value)

	def _identifier(self):
		if self._get_current_char() not in (string.ascii_letters + "_"):
			raise ParseError("Identifier starts with invalid character")
		else:
			identifier = self._get_current_char()
			self.stream_index += 1
		
		while self._get_current_char() in (string.ascii_letters + string.digits + "_"):
			identifier += self._get_current_char()
			self.stream_index += 1

		return Identifier(identifier)

	def _expression(self):
		# Save stream pointer if we need to jump back
		orig_ind = self.stream_index

		# Trim
		self._whitespace()

		# Parse the first term
		term_node = self._term()

		# If parsing fails, jump back
		if term_node is None:
			raise ParseError("Term expected in expression at position {}!".format(self.stream_index))

		# Trim
		self._whitespace()

		expr_op = self._get_current_char()
		while expr_op in "+-":
			self.stream_index += 1

			# Trim
			self._whitespace()

			# Parse the second term
			next_term = self._term()

			# If parsing fails, jump back
			if next_term is None:
				raise ParseError("Term expected in expression at position {0} after {1}!".format(self.stream_index, expr_op))

			# Left-derive expression
			term_node = BinaryExpression(term_node, next_term, self.op_dict[expr_op])

			# Trim
			self._whitespace()

			# Look at whether next character in stream is a expr_op
			expr_op = self._get_current_char()

		return term_node


	def _whitespace(self):
		while len(self.stream) > self.stream_index and self._get_current_char().isspace():
			self.stream_index += 1

	def _number(self):
		orig_index = self.stream_index

		number_str = ""
		while self._get_current_char() in (self.digits + "."):
			number_str += self._get_current_char()
			self.stream_index += 1

		try:
			if number_str == "" or (number_str[0] == "0" and number_str.split(".")[0] != "0"):
				raise ValueError

			number = float(number_str)
			return Number(number)
		except ValueError:
			self.stream_index = orig_index
			raise ParseError("Invalid number")


	def _factor(self):
		orig_index = self.stream_index

		try:
			negateFlag = False
			if self._get_current_char() == "-":
				negateFlag = True
				self.stream_index += 1

			if self._get_current_char() == "(":
				self.stream_index += 1

				node = self._expression()

				if self._get_current_char() != ")":
					self.stream_index = orig_index
					return None
				self.stream_index += 1
			else:
				node = self._number()

			if node is None:
				self.stream_index = orig_index
				return None

			return Factor(node,negateFlag)
		except ParseError:
			return self._assignment()


	def _term(self):
		orig_ind = self.stream_index

		factor_node = self._factor()
		if factor_node is None:
			self.stream_index = orig_ind
			return None

		self._whitespace()

		expr_op = self._get_current_char()
		while expr_op in "*/%":
			self.stream_index += 1

			self._whitespace()

			next_factor = self._factor()
			if next_factor is None:
				self.stream_index = orig_ind
				return None

			factor_node = BinaryExpression(factor_node, next_factor, self.op_dict[expr_op])

			self._whitespace()
			expr_op = self._get_current_char()

		return factor_node

class Evaluator:
	def __init__(self):
		pass
	def eval(self, expression_ast):
		return None

def main():

	arg_parser = argparse.ArgumentParser(description='Evaluate an mathematical expression.')

	# open is used as a type to retrieve a file from the filename given
	arg_parser.add_argument('file', metavar='filename', type=open,
		help='File containing the expression to be evaluated.')

	try:
		args = arg_parser.parse_args()
		expression_parser = Parser()
		evaluator = Evaluator()

		# read every expression from the given file
		for line in args.file:
			try:
				expression_ast = expression_parser.parse(line)
			except ParseError as e:
				print(e)
			else:
				print(expression_ast.eval({}))

	except FileNotFoundError:
		print("Please pass a valid filename")

if __name__ == "__main__":
	main()
