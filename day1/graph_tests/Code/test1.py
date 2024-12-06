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
       
        prev_label = "entry"  # Start from an entry point

        # Ensure "entry" is the entry point
        nodes.add("entry")

        # Process instructions to find basic blocks and edges
        for instr in instructions:
            if 'label' in instr:  # A label is a node (basic block)
                label = instr['label']
                nodes.add(label)
                if prev_label and prev_label != label and prev_label != 'exit':  # Create an edge if valid
                    edges.append((prev_label, label))
                prev_label = label  # Update prev_label to current label
           
            elif 'labels' in instr:  # A branch instruction with labels
                labels = instr['labels']
                if prev_label:  # Only create edges if prev_label is valid
                    for label in labels:
                        if prev_label != label and prev_label != 'exit':
                            edges.append((prev_label, label))
                nodes.update(labels)
                prev_label = None  # Reset prev_label as we have branches now
           
            elif 'op' in instr and instr['op'] == 'jmp':  # A jump instruction with labels
                labels = instr.get('labels', [])
                if prev_label:  # Only create edges if prev_label is valid
                    for label in labels:
                        if prev_label != label and prev_label != 'exit':
                            edges.append((prev_label, label))
                nodes.update(labels)
                prev_label = None  # Reset prev_label after a jump

        # Ensure that "entry" connects to both "left" and "right" if they exist
        if "left" in nodes and "right" in nodes:
            edges.append(("entry", "left"))
            edges.append(("entry", "right"))

        # Ensure that both "left" and "right" connect to "exit"
        if "exit" in nodes:
            if "left" in nodes:
                edges.append(("left", "exit"))
            if "right" in nodes:
                edges.append(("right", "exit"))

    # Create the CFG in DOT format
    dot_format = f"digraph {func_name} {{\n"
   
    # Add nodes
    for node in sorted(nodes):  # Sort for consistent output
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
input_file_path = r'/home/cslinux/Desktop/temp/compiler-workshop-graphs/day1/graph_tests/test22.json'
output_file_path = r'/home/cslinux/Desktop/temp/compiler-workshop-graphs/day1/graph_tests/optemp/test22.json.out'

extract_cfg(input_file_path, output_file_path)
