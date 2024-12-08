import ast

class ForStmtCounter(ast.NodeVisitor):
    current_for_node = None
    stmt_count = 0

    def generic_visit(self, node):
        # If we are inside a for node, count statements
        if self.current_for_node is not None:
            if isinstance(node, ast.stmt):
                self.stmt_count += 1

        # If we just found a new for node, start counting
        elif isinstance(node, ast.For):
            self.current_for_node = node
            self.stmt_count = 0

        super().generic_visit(node)

        # This runs when coming back up from the children
        if node is self.current_for_node:
            # We're done counting this node. Print it out
            print(f'For node contains {self.stmt_count} statements')
            self.current_for_node = None

for_statement_counter = ForStmtCounter()

tree = ast.parse('''
for i in range(10):
    print(i)

for item in items:
    if item == 42:
        print('Magic item found!')
        break
''')
for_statement_counter.visit(tree)