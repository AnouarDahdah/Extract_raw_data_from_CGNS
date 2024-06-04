import h5py

def extract_and_print_data(node, indent=0):
    """Recursively searches for and prints data of meanVxMonitor, meanVyMonitor, and meanVzMonitor nodes."""
    if isinstance(node, h5py.Group):
        for child_name, child_node in node.items():
            if child_name in ["meanVxMonitor", "meanVyMonitor", "meanVzMonitor"]:
                print(f"{'  ' * indent}{child_name}:")
                print_node_data(child_node, indent + 1)
            else:
                extract_and_print_data(child_node, indent + 1)

def print_node_data(node, indent=0):
    """Prints the data of a given node."""
    if isinstance(node, h5py.Dataset):
        print(f"{'  ' * indent}Data: {node[...]}")
    elif isinstance(node, h5py.Group):
        for child_name, child_node in node.items():
            if child_name == 'data':
                print_node_data(child_node, indent)

def main(file_path):
    with h5py.File(file_path, 'r') as f:
        extract_and_print_data(f)

if __name__ == "__main__":
    file_path = "/mnt/c/users/DELL/Downloads/ID2_Volume.cgns"
    main(file_path)
