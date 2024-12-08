import json

def extract_cfg(input_file_path, output_file_path):
    # Read the input JSON file
    with open(input_file_path, 'r') as infile:
        data = json.load(infile)
    
    # Initialize an empty set for nodes and edges
    nodes = set()
    edges = []

    # Extract functions and their instructions
    for func in data.get("functions", []):
        func_name = func.get("name", "main")
        instructions = func.get("instrs", [])
        
        prev_label = None  # Track previous instruction's label for edge creation

        # Process instructions to find basic blocks and edges
        for instr in instructions:
            if 'label' in instr:  # A label is a node (basic block)
                label = instr['label']
                nodes.add(label)
                if prev_label:
                    edges.append((prev_label, label))  # Connect previous label to current one
                prev_label = label  # Set current label as the previous one for the next instructions
            elif 'labels' in instr:  # A branch instruction with labels
                labels = instr['labels']
                if prev_label:
                    # Add edges from the previous label to each of the branch labels
                    for label in labels:
                        edges.append((prev_label, label))
                nodes.update(labels)
                prev_label = None  # Reset prev_label as we have branches now
            elif 'op' in instr and instr['op'] == 'jmp':  # A jump instruction with labels
                labels = instr.get('labels', [])
                if prev_label:
                    # Add edges from the previous label to each of the jump target labels
                    for label in labels:
                        edges.append((prev_label, label))
                nodes.update(labels)
                prev_label = None  # Reset prev_label after a jump

    # Create the CFG in DOT format
    dot_format = f"digraph {func_name} {{\n"
    
    # Add nodes sorted for consistent output
    for node in sorted(nodes):
        dot_format += f'  "{node}";\n'
    
    # Add edges without duplicates
    unique_edges = set(edges)  # Use a set to avoid duplicates
    for edge in unique_edges:
        dot_format += f'  "{edge[0]}" -> "{edge[1]}";\n'
    
    dot_format += "}\n"

    # Write the output to a file
    with open(output_file_path, 'w') as outfile:
        outfile.write(dot_format)

# Example usage for Test Input 5
input_file_path = r'C:\Users\Aakash V\Documents\GitHub\compiler-workshop-graphs\day1\graph_tests\test5.json'
output_file_path = r'C:\Users\Aakash V\Documents\GitHub\compiler-workshop-graphs\day1\graph_tests\Output\test5.json.out'

extract_cfg(input_file_path, output_file_path)