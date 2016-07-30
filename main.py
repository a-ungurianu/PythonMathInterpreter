import argparse, os

class Parser:
	def __init__(self):
		pass
	def parse(self,exp_string):
		pass


def main():
	arg_parser = argparse.ArgumentParser(description='Evaluate an mathematical expression.')
	arg_parser.add_argument('file', metavar='filename', type=open, 
		help='File containing the expression to be evaulated.')
	
	try:
		args = arg_parser.parse_args()
		expression_parser = Parser()
		for line in args.file:
			expression_parser.parse(line)
	except FileNotFoundError:
		print("Please pass a valid filename")

if __name__ == "__main__":
	main()
