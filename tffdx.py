import numpy as np
import pandas as pd
import os
from pygem import FFD
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from scipy.spatial import KDTree

def read_csv_to_array(filename):
    df = pd.read_csv(filename)
    return df.to_numpy()

# Function to calculate deformation parameters
def calculate_deformation_parameters(mesh_original, mesh_target, grid_size):
    # Determine the bounding box of the original mesh
    bbox_min = np.min(mesh_original, axis=0)
    bbox_max = np.max(mesh_original, axis=0)
    bbox_length = bbox_max - bbox_min
    
    # Set up the FFD with a specified grid size
    ffd = FFD(grid_size)
    ffd.box_length = bbox_length
    ffd.box_origin = bbox_min
    
    # Initialize control points for transformation
    initial_mu_x = np.zeros_like(ffd.array_mu_x)
    initial_mu_y = np.zeros_like(ffd.array_mu_y)
    initial_mu_z = np.zeros_like(ffd.array_mu_z)
    
    final_mu_x = np.copy(initial_mu_x)
    final_mu_y = np.copy(initial_mu_y)
    final_mu_z = np.copy(initial_mu_z)
    
    # Calculate mean differences for the central control point if it exists
    if all(size > 1 for size in grid_size):
        center_indices = tuple(size // 2 for size in grid_size)
        final_mu_x[center_indices] = (np.mean(mesh_target[:, 0]) - np.mean(mesh_original[:, 0])) / bbox_length[0]
        final_mu_y[center_indices] = (np.mean(mesh_target[:, 1]) - np.mean(mesh_original[:, 1])) / bbox_length[1]
        final_mu_z[center_indices] = (np.mean(mesh_target[:, 2]) - np.mean(mesh_original[:, 2])) / bbox_length[2]

    # Set the final control points for FFD
    ffd.array_mu_x = final_mu_x
    ffd.array_mu_y = final_mu_y
    ffd.array_mu_z = final_mu_z
    
    # Apply FFD transformations
    new_mesh = ffd(mesh_original)
    
    # Use KDTree to match the number of points in new_mesh to mesh_target
    kdtree = KDTree(new_mesh)
    _, indices = kdtree.query(mesh_target)
    new_mesh_interpolated = new_mesh[indices]
    
    # Calculate mean squared error between target and transformed mesh
    mse = np.mean((mesh_target - new_mesh_interpolated) ** 2)
    
    return new_mesh_interpolated, mse

# Function to plot and save the mesh
def plot_and_save_meshes(mesh1, mesh2, title1, title2, filename):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(mesh1[:, 0], mesh1[:, 1], mesh1[:, 2], s=1, color='blue', label=title1)
    ax.scatter(mesh2[:, 0], mesh2[:, 1], mesh2[:, 2], s=1, color='red', label=title2)
    ax.set_title(f'{title1} and {title2}')
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.legend()
    plt.savefig(filename)
    plt.close()

# Prompt the user to enter the paths for the original and target CSV files
filename_original = input("Enter the path of the original CSV file: ")
filename_target = input("Enter the path of the target CSV file: ")

# Read the mesh data from the CSV files
mesh_original = read_csv_to_array(filename_original)
mesh_target = read_csv_to_array(filename_target)

# List to store accuracy values
accuracy_values = []
control_points = []

# Calculate maximum possible error (sum of squared distances to the farthest point)
max_possible_error = np.sum((np.max(mesh_target, axis=0) - np.min(mesh_target, axis=0))**2)

# Incrementally increase the number of control points and calculate accuracy
previous_accuracy = 0
improvement_threshold = 0.01
max_control_points = 1000

for i in range(1, 11):
    grid_size = [i, i, i]
    new_mesh, mse = calculate_deformation_parameters(mesh_original, mesh_target, grid_size)
    accuracy = 100 * (1 - mse / max_possible_error)
    accuracy_values.append(accuracy)
    control_points.append(i**3)
    
    # Stop if improvement is less than the threshold
    if accuracy - previous_accuracy < improvement_threshold:
        break
    previous_accuracy = accuracy

# Plot the accuracy of the transformation using Matplotlib
plt.figure()
plt.plot(control_points, accuracy_values, marker='o')
plt.title('Accuracy of Transformation vs. Number of Control Points')
plt.xlabel('Number of Control Points')
plt.ylabel('Accuracy (%)')
plt.grid(True)
accuracy_plot_file = os.path.splitext(filename_original)[0] + "_accuracy_plot.png"
plt.savefig(accuracy_plot_file)
plt.close()

print(f"PNG file (Accuracy Plot) has been saved: {accuracy_plot_file}")

# Plot and save the original and transformed meshes overlaid
overlay_plot_file = os.path.splitext(filename_original)[0] + "_overlay.png"
plot_and_save_meshes(mesh_target, new_mesh, 'Target Mesh', 'Transformed Mesh', overlay_plot_file)

print(f"PNG file (Overlay of Target and Transformed Meshes) has been saved: {overlay_plot_file}")
