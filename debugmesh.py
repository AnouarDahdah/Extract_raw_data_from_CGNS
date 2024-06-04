from pathlib import Path
import CGNS.MAP
import vtk

def sorted_nicely(l):
    """Sort the given iterable in the way that humans expect."""
    import re
    convert = lambda text: int(text) if text.isdigit() else text.lower()
    alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)]
    return sorted(l, key=alphanum_key)

def zone_extractor(fname: str) -> list:
    """This function extracts all the zones in a CGNS file

    Args:
        fname (str): Path to the CGNS file

    Returns:
        list: List of zone names
    """
    (tree, links, paths) = CGNS.MAP.load(Path(fname))
    zones = []
    for node in tree:
        if (node is not None) and isinstance(node, list) and (node[1][0] == 'Base'):
            zones = [child[0] for child in node[1][2] if child[0].startswith('Zone')]
    return sorted_nicely(zones)

def extract_mesh_from_zone(tree, zone_name: str) -> tuple:
    """Extracts mesh data for a given zone name from the CGNS file.

    Args:
        tree (list): The CGNS tree structure
        zone_name (str): The name of the zone to extract mesh from

    Returns:
        tuple: Coordinates and connectivity arrays
    """
    import numpy as np
    
    coordinates = None
    connectivity = None

    for node in tree:
        if (node is not None) and isinstance(node, list) and (node[1][0] == 'Base'):
            for child in node[1][2]:
                if child[0] == zone_name:
                    for grandchild in child[2]:
                        if grandchild[0] == 'GridCoordinates':
                            coordinates = []
                            for gc in grandchild[2]:
                                if gc[0].startswith('Coordinate'):
                                    coordinates.append(gc[1])
                            coordinates = np.array(coordinates)
                        elif grandchild[0] == 'Elements':
                            connectivity = grandchild[1]
    return coordinates, connectivity

def save_mesh_to_vtk(coordinates, connectivity, zone_name):
    """Saves mesh data to VTK format.

    Args:
        coordinates (np.ndarray): Array of coordinates
        connectivity (list): Connectivity information
        zone_name (str): Name of the zone
    """
    points = vtk.vtkPoints()
    cells = vtk.vtkCellArray()

    for point in coordinates:
        points.InsertNextPoint(point)

    for cell_conn in connectivity:
        if len(cell_conn) > 0:
            vtk_cell = vtk.vtkPolygon()
            for point_id in cell_conn:
                vtk_cell.GetPointIds().InsertNextId(point_id - 1)  # CGNS indexing starts from 1
            cells.InsertNextCell(vtk_cell)

    polydata = vtk.vtkPolyData()
    polydata.SetPoints(points)
    polydata.SetPolys(cells)

    writer = vtk.vtkPolyDataWriter()
    writer.SetFileName(f"{zone_name}.vtk")
    writer.SetInputData(polydata)
    
    try:
        writer.Write()
        print(f"Saved {zone_name}.vtk successfully.")
    except Exception as e:
        print(f"Error occurred while saving {zone_name}.vtk: {e}")

def main(fname: str):
    zones = zone_extractor(fname)
    (tree, _, _) = CGNS.MAP.load(Path(fname))
    
    for zone in zones:
        print(f"Extracting mesh data for zone: {zone}")
        coordinates, connectivity = extract_mesh_from_zone(tree, zone)
        if coordinates is not None and connectivity is not None:
            print(f"Mesh data extracted successfully for zone: {zone}")
            save_mesh_to_vtk(coordinates, connectivity, zone)
        else:
            print(f"Failed to extract mesh data for zone: {zone}")

if __name__ == "__main__":
    fname = "/home/adahdah/ID2_Surface1.cgns"
    main(fname)
