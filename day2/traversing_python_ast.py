import ast
import argparse

class MyVisitor(ast.NodeVisitor):
    def generic_visit(self, node):
        print(f"Entering {node.__class__.__name__}")
        super().generic_visit(node)  

parser = argparse.ArgumentParser()
parser.add_argument('filename', type=str)
args = parser.parse_args()

with open(args.filename, 'r') as file:
    code = file.read()
tree = ast.parse(code)
print(ast.dump(tree, indent=3))
print("\n")
visitor = MyVisitor()
visitor.visit(tree)


	
