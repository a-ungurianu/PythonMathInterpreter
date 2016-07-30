import argparse, os

class Tokenizer:
	def __init__(self):
		pass
	def tokenize(self, exp_string):
		return []

class ASTNode(object):

	def __init__(self):
		pass

	def eval():
		raise NotImplementedError

class Expression(ASTNode):

	def __init__(self, first_term, second_term, operation):
		self.first_term = first_term
		self.second_term = second_term
		self.operation = operation

	def eval():
		return self.operation(self.first_term, self.second_term)


class Parser:

	op_dict = { "+": lambda a, b: a + b,
				"-": lambda a, b: a - b,
				"*": lambda a, b: a * b,
				"/": lambda a, b: a / b}

	def __init__(self):
		self.stream = ""

	def parse(self, exp_string):
		self.stream_index = 0
		self.stream = exp_string

		ast = self._expression()


	def _expression(self):
		# Save stream pointer if we need to jump back
		orig_ind = self.stream_index

		# Trim
		self._whitespace()

		# Parse the first term
		term_node = self._term()

		# If parsing fails, jump back
		if term_node is None:
			self.stream_index = orig_ind
			return None

		# Trim
		self._whitespace()

		expr_op = self.stream[self.stream_index]
		while expr_op in "+-":
			self.stream_index += 1

			# Trim
			self._whitespace()

			# Parse the second term
			next_term = self._term()

			# If parsing fails, jump back
			if next_term is None:
				self.stream_index = orig_ind
				return None

			term_node = Expression(term_node, next_term, op_dict[expr_op])

			# Trim
			_whitespace()

			# Look at whether next character in stream is a expr_op
			expr_op = self.stream[self.stream_index]




	def _whitespace(self):
		while self.stream[self.stream_index].isspace():
			self.stream_index += 1

	def _number(self):
		print(stream_index)

	def _factor(self):
		pass

	def _term(self):
		pass

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
			expression_ast = expression_parser.parse(line)
			print(evaluator.eval(expression_ast))

	except FileNotFoundError:
		print("Please pass a valid filename")

if __name__ == "__main__":
	main()
