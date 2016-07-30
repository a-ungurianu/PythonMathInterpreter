import argparse, os

class Parser:
	def __init__(self):
		pass
	def parse(self,exp_string):
		pass

class Evaluator:
	def __init__(self):
		pass
	def eval(self,expression_ast):
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
