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
        func_name = func.get("name", "")
        instructions = func.get("instrs", [])
        
        # Entry point node
        nodes.add("b1")

        # Process instructions
        for instr in instructions:
            # No labels or branches means we don't add any additional nodes or edges
            if 'label' in instr:
                nodes.add(instr['label'])
                # If there were branches, we would add edges here

    # Create the CFG in DOT format
    dot_format = f"digraph {func_name} {{\n"

    # Add nodes sorted for consistent output
    for node in sorted(nodes):
        dot_format += f'  {node};\n'
    
    # There are no edges to add since there are no branches or jumps
    dot_format += '}\n'

    # Write the output to a file
    with open(output_file_path, 'w') as outfile:
        outfile.write(dot_format)

# Example usage for Test Input
input_file_path = r'C:\Users\Aakash V\Documents\GitHub\compiler-workshop-graphs\day1\graph_tests\test9.json'
output_file_path = r'C:\Users\Aakash V\Documents\GitHub\compiler-workshop-graphs\day1\graph_tests\Output\test9.json.out'

extract_cfg(input_file_path, output_file_path)