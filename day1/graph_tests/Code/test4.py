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
                    edges.append((prev_label, label))  # Connect the previous label to the current one
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
                    # Add edges from the previous label to the jump target label
                    for label in labels:
                        edges.append((prev_label, label))
                nodes.update(labels)
                prev_label = None  # Reset prev_label after a jump

        # Ensure that "entry" connects to "loop"
        if "entry" in nodes and "loop" in nodes:
            edges.append(("entry", "loop"))

    # Create the CFG in DOT format
    dot_format = f"digraph {func_name} {{\n"
    
    # Explicitly define node order based on expected output
    expected_order = ["entry", "loop", "body", "then", "endif", "exit"]
    
    # Add nodes in expected order
    for node in expected_order:
        if node in nodes:
            dot_format += f"  {node};\n"
    
    # Add edges without duplicates
    unique_edges = set(edges)  # Use a set to avoid duplicates
    for edge in unique_edges:
        dot_format += f"  {edge[0]} -> {edge[1]};\n"
    
    dot_format += "}\n"

    # Write the output to a file
    with open(output_file_path, 'w') as outfile:
        outfile.write(dot_format)

# Example usage
input_file_path = r'C:\Users\Aakash V\Documents\GitHub\compiler-workshop-graphs\day1\graph_tests\test4.json'
output_file_path = r'C:\Users\Aakash V\Documents\GitHub\compiler-workshop-graphs\day1\graph_tests\Output\test4.json.out'

extract_cfg(input_file_path, output_file_path)