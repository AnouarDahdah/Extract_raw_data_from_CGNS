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
file_pattern = 'coordinate_data_part21.csv'

# Generate the filename for part 21
filename = os.path.join(file_dir, file_pattern)

# Read the mesh data from the CSV file
mesh = read_csv_to_array(filename)

# Determine the bounding box of the mesh
bbox_min = np.min(mesh, axis=0)
bbox_max = np.max(mesh, axis=0)
bbox_length = bbox_max - bbox_min

# Set up the FFD with more control points (4x4x4 grid)
ffd = FFD([2, 2, 2])
ffd.box_length = bbox_length
ffd.box_origin = bbox_min

# Apply some transformations (example transformations)
ffd.array_mu_x[1, 0, 1] = bbox_length[0] / 1.10  # Example transformation
ffd.array_mu_x[1, 1, 1] = bbox_length[0] / 0.90  # Example transformation
ffd.array_mu_x[0, 1, 1] = bbox_length[0] / 1.50  # Example transformation
ffd.array_mu_y[0, 1, 1] = bbox_length[0] / 1.50  # Example transformation
ffd.array_mu_z[0, 0, 1] = bbox_length[2] / 2.3  # Example transformation

# Apply FFD transformations
new_mesh = ffd(mesh)

# Create a figure for the original and deformed meshes without control points
fig = go.Figure()

# Add original mesh
fig.add_trace(go.Scatter3d(
    x=mesh[:, 0], y=mesh[:, 1], z=mesh[:, 2],
    mode='markers',
    marker=dict(size=2, color='blue'),
    name='Original Mesh'
))

# Add deformed mesh
fig.add_trace(go.Scatter3d(
    x=new_mesh[:, 0], y=new_mesh[:, 1], z=new_mesh[:, 2],
    mode='markers',
    marker=dict(size=2, color='green'),
    name='Deformed Mesh'
))

# Update the layout
fig.update_layout(scene=dict(xaxis_title="X Axis", yaxis_title="Y Axis", zaxis_title="Z Axis"))

# Add annotation for Original Mesh and Deformed Mesh
fig.add_annotation(
    x=0.5, y=-0.15, xref='paper', yref='paper', showarrow=False,
    text="Original Mesh (Blue) and Deformed Mesh (Green)",
    font=dict(size=12)
)

# Save the plot to an HTML file
output_file = os.path.join(file_dir, "superimposed_mesh_without_control_points_part21.html")
fig.write_html(output_file)

print(f"HTML file for part 21 (Superimposed Original and Deformed Mesh without Control Points) has been saved: {output_file}")
