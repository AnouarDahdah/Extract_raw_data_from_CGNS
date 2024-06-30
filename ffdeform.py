import numpy as np
import pandas as pd
import plotly.graph_objects as go
from pygem import FFD
import os

def read_csv_to_array(filename):
    df = pd.read_csv(filename)
    return df.to_numpy()

# Directory and file pattern
file_dir = '/home/adahdah/'
file_pattern = 'coordinate_data_part{}.csv'

<<<<<<< HEAD
for i in range(1, 22):
=======
for i in range(1, 21):
>>>>>>> 6be856d286fc8ffc14c15663bd6353c128f54fa9
    # Generate the filename
    filename = os.path.join(file_dir, file_pattern.format(i))
    
    # Read the mesh data from the CSV file
    mesh = read_csv_to_array(filename)
    
    # Determine the bounding box of the mesh
    bbox_min = np.min(mesh, axis=0)
    bbox_max = np.max(mesh, axis=0)
    bbox_length = bbox_max - bbox_min
    
    # Set up the FFD
    ffd = FFD([2, 2, 2])
    ffd.box_length = bbox_length
    ffd.box_origin = bbox_min
    
    # Apply some transformations
<<<<<<< HEAD
    ffd.array_mu_x[1, 1, 1] = bbox_length[0] / 1  # Example transformation
    ffd.array_mu_y[1, 1, 1] = bbox_length[1] / 1  # Example transformation
    ffd.array_mu_z[1, 1, 1] = bbox_length[2] / 1  # Example transformation
    
=======
    ffd.array_mu_x[1, 1, 1] = bbox_length[0] / 0.2  # Example transformation
    ffd.array_mu_z[1, 1, 1] = bbox_length[2] / 20  # Example transformation
>>>>>>> 6be856d286fc8ffc14c15663bd6353c128f54fa9
    
    # Apply FFD transformations
    new_mesh = ffd(mesh)
    
    # Prompt for user choice
    choice = input(f"Choose which mesh to save for part {i} (1: Original, 2: Transformed): ")
    
    if choice == '1':
        # Create a figure for the original mesh with control points
        fig = go.Figure()
        fig.add_trace(go.Scatter3d(
            x=mesh[:, 0], y=mesh[:, 1], z=mesh[:, 2],
            mode='markers',
            marker=dict(size=2, color='blue'),
            name='Original Mesh'
        ))
        
        # Add control points
        control_points = ffd.control_points()
        fig.add_trace(go.Scatter3d(
            x=control_points[:, 0], y=control_points[:, 1], z=control_points[:, 2],
            mode='markers',
            marker=dict(size=5, color='red'),
            name='Control Points'
        ))
        
        # Update the layout to remove annotations and legend
        fig.update_layout(scene=dict(xaxis_title="X Axis", yaxis_title="Y Axis", zaxis_title="Z Axis"))
        
        # Add annotation for Original Mesh
        fig.add_annotation(
            x=0.5, y=-0.15, xref='paper', yref='paper', showarrow=False,
            text="Original Mesh", font=dict(size=12)
        )
        
        # Save the plot to an HTML file
        output_file = os.path.join(file_dir, f"original_mesh_part{i}.html")
        fig.write_html(output_file)

        print(f"HTML file for part {i} (Original Mesh with Control Points) has been saved: {output_file}")
        
    elif choice == '2':
        # Create a figure for the transformed mesh with control points
        fig = go.Figure()
        fig.add_trace(go.Scatter3d(
            x=new_mesh[:, 0], y=new_mesh[:, 1], z=new_mesh[:, 2],
            mode='markers',
            marker=dict(size=2, color='green'),
            name='Deformed Mesh'
        ))

        # Add control points
        control_points = ffd.control_points()
        fig.add_trace(go.Scatter3d(
            x=control_points[:, 0], y=control_points[:, 1], z=control_points[:, 2],
            mode='markers',
            marker=dict(size=5, color='red'),
            name='Control Points'
        ))

        # Update the layout to remove annotations and legend
        fig.update_layout(scene=dict(xaxis_title="X Axis", yaxis_title="Y Axis", zaxis_title="Z Axis"))
        
        # Add annotation for Transformed Mesh
        fig.add_annotation(
            x=0.5, y=-0.15, xref='paper', yref='paper', showarrow=False,
            text="Deformed Mesh", font=dict(size=12)
        )
        
        # Save the plot to an HTML file
        output_file = os.path.join(file_dir, f"transformed_mesh_part{i}.html")
        fig.write_html(output_file)

        print(f"HTML file for part {i} (Transformed Mesh with Control Points) has been saved: {output_file}")
        
    else:
        print("Invalid choice. Please enter 1 or 2.")
