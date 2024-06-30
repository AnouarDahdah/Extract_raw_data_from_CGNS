import numpy as np
import pandas as pd
import os
from pygem import FFD
import plotly.graph_objects as go

def read_csv_to_array(filename):
    df = pd.read_csv(filename)
    return df.to_numpy()

# Directory and file pattern for original and target designs
file_dir = '/home/adahdah/'
file_pattern_original = 'coordinate_data_part{}.csv'
file_pattern_target = 'coordinate_datad2_part{}.csv'

# Function to calculate deformation parameters
def calculate_deformation_parameters(mesh_original, mesh_target):
    # Determine the bounding box of the original mesh
    bbox_min = np.min(mesh_original, axis=0)
    bbox_max = np.max(mesh_original, axis=0)
    bbox_length = bbox_max - bbox_min
    
    # Set up the FFD with a default grid size
    ffd = FFD([2, 2, 2])
    ffd.box_length = bbox_length
    ffd.box_origin = bbox_min
    
    # Initialize control points for transformation
    initial_mu_x = np.zeros_like(ffd.array_mu_x)
    initial_mu_y = np.zeros_like(ffd.array_mu_y)
    initial_mu_z = np.zeros_like(ffd.array_mu_z)
    
    final_mu_x = np.copy(initial_mu_x)
    final_mu_y = np.copy(initial_mu_y)
    final_mu_z = np.copy(initial_mu_z)
    
    final_mu_x[1, 1, 1] = (np.mean(mesh_target[:, 0]) - np.mean(mesh_original[:, 0])) / bbox_length[0]
    final_mu_y[1, 1, 1] = (np.mean(mesh_target[:, 1]) - np.mean(mesh_original[:, 1])) / bbox_length[1]
    final_mu_z[1, 1, 1] = (np.mean(mesh_target[:, 2]) - np.mean(mesh_original[:, 2])) / bbox_length[2]

    # Set the final control points for FFD
    ffd.array_mu_x = final_mu_x
    ffd.array_mu_y = final_mu_y
    ffd.array_mu_z = final_mu_z
    
    # Apply FFD transformations
    new_mesh = ffd(mesh_original)
    
    # Extract deformation parameters
    deformation_parameters = {
        'mu_x': ffd.array_mu_x,
        'mu_y': ffd.array_mu_y,
        'mu_z': ffd.array_mu_z,
        'number_of_control_points': ffd.n_control_points
    }
    
    return new_mesh, deformation_parameters, ffd

# Prompt the user to choose the number of the CSV file to process
file_number = int(input("Enter the number of the CSV file to process (1-20): "))

# Generate the filenames
filename_original = os.path.join(file_dir, file_pattern_original.format(file_number))
filename_target = os.path.join(file_dir, file_pattern_target.format(file_number))

# Read the mesh data from the CSV files
mesh_original = read_csv_to_array(filename_original)
mesh_target = read_csv_to_array(filename_target)

# Calculate the deformation parameters and the final transformed mesh
new_mesh, deformation_parameters, ffd = calculate_deformation_parameters(mesh_original, mesh_target)

# Print the deformation parameters
print(f"Deformation parameters for part {file_number}:")
print(f"mu_x: {deformation_parameters['mu_x']}")
print(f"mu_y: {deformation_parameters['mu_y']}")
print(f"mu_z: {deformation_parameters['mu_z']}")
print(f"Number of control points: {deformation_parameters['number_of_control_points']}")

# Create a figure for the original and transformed meshes with control points
fig = go.Figure()

# Add original mesh
fig.add_trace(go.Scatter3d(
    x=mesh_original[:, 0], y=mesh_original[:, 1], z=mesh_original[:, 2],
    mode='markers',
    marker=dict(size=2, color='blue'),
    name='Original Mesh'
))

# Add transformed mesh
fig.add_trace(go.Scatter3d(
    x=new_mesh[:, 0], y=new_mesh[:, 1], z=new_mesh[:, 2],
    mode='markers',
    marker=dict(size=2, color='green'),
    name='Transformed Mesh'
))

# Extract control points from the FFD object
control_points = np.vstack([ffd.array_mu_x.flatten(), ffd.array_mu_y.flatten(), ffd.array_mu_z.flatten()]).T

# Add control points
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
    text="Transformed Mesh", font=dict(size=12)
)

# Save the plot to an HTML file
output_file = os.path.join(file_dir, f"transformed_mesh_part{file_number}.html")
fig.write_html(output_file)

print(f"HTML file for part {file_number} (Transformed Mesh with Control Points) has been saved: {output_file}")