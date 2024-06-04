import vtk
import CGNS.MAP
import CGNS.PAT.cgnsutils as CGU

def print_tree(node, indent=0):
    """Print the CGNS tree structure for debugging."""
    if node is not None:
        print("  " * indent + str(node))
        if isinstance(node, list) and len(node) > 2 and isinstance(node[2], list):
            for child in node[2]:
                print_tree(child, indent + 1)

def find_base_nodes(node, base_nodes):
    """Recursively find 'CGNSBase_t' nodes in the CGNS tree."""
    if node is not None:
        if isinstance(node, list) and len(node) > 0:
            if node[0] == 'CGNSBase_t':
                base_nodes.append(node)
            elif len(node) > 2 and isinstance(node[2], list):
                for child in node[2]:
                    find_base_nodes(child, base_nodes)

def get_base_nodes(tree):
    """Find base nodes in the CGNS tree."""
    base_nodes = []
    find_base_nodes(tree, base_nodes)
    print(f"Base nodes found: {len(base_nodes)}")
    return base_nodes

def get_zone_nodes(base_node):
    """Find zone nodes under a given base node."""
    zone_nodes = []
    try:
        if base_node is not None and len(base_node) > 2:
            for child_node in base_node[2]:
                if child_node is not None:
                    print(f"Checking child node: {child_node[0]}")
                    if child_node[0] == 'Zone_t':
                        zone_nodes.append(child_node)
    except TypeError as e:
        print(f"TypeError in get_zone_nodes: {e}")
    print(f"Zone nodes found: {len(zone_nodes)}")
    return zone_nodes

def get_grid_coordinates(zone_node):
    """Extract grid coordinates from a given zone node."""
    coords = [[], [], []]
    try:
        if zone_node is not None and len(zone_node) > 2:
            for child_node in zone_node[2]:
                if child_node is not None and child_node[0] == 'GridCoordinates_t':
                    for grandchild_node in child_node[2]:
                        if grandchild_node is not None and grandchild_node[0] == 'DataArray_t':
                            if grandchild_node[1] == 'CoordinateX':
                                coords[0] = grandchild_node[2]
                            elif grandchild_node[1] == 'CoordinateY':
                                coords[1] = grandchild_node[2]
                            elif grandchild_node[1] == 'CoordinateZ':
                                coords[2] = grandchild_node[2]
    except TypeError as e:
        print(f"TypeError in get_grid_coordinates: {e}")
    print(f"Coordinates found: X({len(coords[0])}), Y({len(coords[1])}), Z({len(coords[2])})")
    return coords

def get_elements(zone_node):
    """Extract elements from a given zone node."""
    elements = []
    try:
        if zone_node is not None and len(zone_node) > 2:
            for child_node in zone_node[2]:
                if child_node is not None and child_node[0] == 'Elements_t':
                    for grandchild_node in child_node[2]:
                        if grandchild_node is not None and grandchild_node[0] == 'DataArray_t':
                            elements = grandchild_node[2]
    except TypeError as e:
        print(f"TypeError in get_elements: {e}")
    print(f"Elements found: {len(elements)}")
    return elements

def extract_mesh(tree):
    mesh_data = {}
    
    base_nodes = get_base_nodes(tree)
    for base_node in base_nodes:
        print(f"Processing base node: {base_node[1]}")
        zone_nodes = get_zone_nodes(base_node)
        for zone_node in zone_nodes:
            print(f"Processing zone node: {zone_node[1]}")
            coords = get_grid_coordinates(zone_node)
            elements = get_elements(zone_node)
            mesh_data[zone_node[1]] = {
                'coordinates': coords,
                'elements': elements
            }
    
    return mesh_data

try:
    # Load CGNS file
    (tree, links, paths) = CGNS.MAP.load("/home/adahdah/ID2_Surface1.cgns")
    if tree is not None:
        print("Tree loaded successfully")
        print("Tree structure:")
        print_tree(tree)  # Print the entire tree structure for debugging
        
        # Extract mesh
        mesh = extract_mesh(tree)
        print("Mesh data:", mesh)  # Diagnostic print statement
        
        # Save mesh data to VTK file
        for zone, data in mesh.items():
            points = vtk.vtkPoints()
            for i in range(len(data['coordinates'][0])):
                points.InsertNextPoint(data['coordinates'][0][i], data['coordinates'][1][i], data['coordinates'][2][i])
            
            mesh_cells = vtk.vtkCellArray()
            for element in data['elements']:
                cell = vtk.vtkHexahedron()  # Assuming hexahedral elements
                for i in range(8):  # Assuming 8 nodes per hexahedral element
                    cell.GetPointIds().SetId(i, element[i])
                mesh_cells.InsertNextCell(cell)
            
            mesh_polydata = vtk.vtkPolyData()
            mesh_polydata.SetPoints(points)
            mesh_polydata.SetPolys(mesh_cells)
            
            writer = vtk.vtkXMLPolyDataWriter()
            output_filename = f"{zone}.vtk"
            writer.SetFileName(output_filename)
            writer.SetInputData(mesh_polydata)
            writer.Write()
            print(f"Saved VTK file: {output_filename}")
    else:
        print("Error: Failed to load CGNS tree.")
except Exception as e:
    print("An error occurred:", e)
