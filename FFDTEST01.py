import meshio
import numpy as np
import matplotlib.pyplot as plt
from pygem.vffd import VFFD, _volume

# Read the mesh
mesh = meshio.read("/home/adahdah/dataCADtest10.stl")
points = mesh.points
faces = mesh.cells_dict["triangle"]

# Normalize points
points = points - np.min(points) + 0.1
points = points / np.max(points)
points = 0.95 * points
points[:, 1] = points[:, 1] - np.min(points[:, 1])

# Initialize VFFD
initvolume = _volume(points, faces)
vffd = VFFD(faces, np.array(initvolume), [2, 2, 2])

# Apply random deformations
np.random.seed(0)
vffd.array_mu_x = vffd.array_mu_x + 0.5 * np.random.rand(2, 2, 2)
vffd.array_mu_y = vffd.array_mu_y + 0.5 * np.random.rand(2, 2, 2)
vffd.array_mu_z = vffd.array_mu_z + 0.5 * np.random.rand(2, 2, 2)

# Function to calculate percentage difference
def percentage_difference(original, deformed):
    return np.linalg.norm(deformed - original) / np.linalg.norm(original) * 100

# Set up the plot
fig = plt.figure(figsize=plt.figaspect(0.5))
ax = fig.add_subplot(1, 2, 1, projection='3d')

# Deform mesh in steps and visualize progress
steps = 10
for step in range(steps + 1):
    # Adjust control points based on the step
    fraction = step / steps
    vffd_temp = VFFD(faces, np.array(initvolume), [2, 2, 2])
    vffd_temp.array_mu_x = vffd.array_mu_x * fraction
    vffd_temp.array_mu_y = vffd.array_mu_y * fraction
    vffd_temp.array_mu_z = vffd.array_mu_z * fraction
    vffd_temp.adjust_control_points(points)
    
    # Get the deformed mesh
    mesh_def = vffd_temp(points).reshape(points.shape)
    
    # Calculate percentage difference
    perc_diff = percentage_difference(points, mesh_def)
    
    # Update plot
    ax.clear()
    ax.plot_trisurf(mesh_def[:, 0], mesh_def[:, 1], mesh_def[:, 2], triangles=faces, cmap=plt.cm.Spectral)
    ax.set_title(f'Deformed Mesh - Step {step}/{steps} - {perc_diff:.2f}% Difference')
    plt.pause(0.5)  # Pause to update the plot

# Final percentage difference
final_diff = percentage_difference(points, mesh_def)
print("Final percentage difference from the original mesh is", final_diff)

# Show the final plot
plt.show()
