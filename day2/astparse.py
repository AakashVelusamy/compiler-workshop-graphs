import ast
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('filename', type=str)
args = parser.parse_args()
with open(args.filename, 'r') as file: 
    code = file.read()
tree = ast.parse(code)
print(ast.dump(tree, indent=2))


	
