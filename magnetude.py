import h5py
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.colors import Normalize

# Open the CGNS file containing mesh data
cgns_file = h5py.File("/home/adahdah/ID2_Surface15.cgns", "r")

# Define the path to the grid coordinates
grid_coordinates_path = "/Base/Air Body/GridCoordinates"
# Define the path to the interfaces
WSSxPath = "/Base/Air Body/Solution00001/meanWSSxMonitor"
WSSyPath = "/Base/Air Body/Solution00001/meanWSSyMonitor"
WSSzPath = "/Base/Air Body/Solution00001/meanWSSzMonitor"

# Extract grid coordinates from the CGNS file
x_dataset = np.array(cgns_file[grid_coordinates_path + "/CoordinateX/ data"])
y_dataset = np.array(cgns_file[grid_coordinates_path + "/CoordinateY/ data"])
z_dataset = np.array(cgns_file[grid_coordinates_path + "/CoordinateZ/ data"])

# Extract wall shear stress components from the CGNS file
WSSx = np.array(cgns_file[WSSxPath + "/ data"])
WSSy = np.array(cgns_file[WSSyPath + "/ data"])
WSSz = np.array(cgns_file[WSSzPath + "/ data"])

# Trim the WSS datasets to match the length of the coordinate datasets
min_length = min(x_dataset.shape[0], WSSx.shape[0])

x_dataset = x_dataset[:min_length]
y_dataset = y_dataset[:min_length]
z_dataset = z_dataset[:min_length]
WSSx = WSSx[:min_length]
WSSy = WSSy[:min_length]
WSSz = WSSz[:min_length]

# Normalize WSS magnitude to the range [0, 1] for coloring
WSS_magnitude = np.sqrt(WSSx**2 + WSSy**2 + WSSz**2)
norm = Normalize(vmin=0, vmax=1)
WSS_magnitude_normalized = norm(WSS_magnitude)

# Print the extracted float values
print("X coordinates:")
print(x_dataset)
print("\nY coordinates:")
print(y_dataset)
print("\nZ coordinates:")
print(z_dataset)
print("\nWSSX:")
print(WSSx)
print("\nWSSY")
print(WSSy)
print("\nWSSZ")
print(WSSz)
print("\nWSS Magnitude:")
print(WSS_magnitude)
print("\nNormalized WSS Magnitude:")
print(WSS_magnitude_normalized)

# Create a 3D scatter plot
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Scatter plot of the points with colors based on normalized WSS magnitude
sc = ax.scatter(x_dataset, y_dataset, z_dataset, c=WSS_magnitude_normalized, cmap='viridis', marker='o')

# Add quiver plot to show WSS vectors
ax.quiver(x_dataset, y_dataset, z_dataset, WSSx, WSSy, WSSz, length=0.01, normalize=True, color='r')

# Optionally set labels
ax.set_xlabel('X Coordinate')
ax.set_ylabel('Y Coordinate')
ax.set_zlabel('Z Coordinate')

# Set title
ax.set_title('3D Scatter Plot with WSS Vectors')

# Add a color bar which maps values to colors
color_bar = plt.colorbar(sc, ax=ax, label='Normalized WSS Magnitude')
color_bar.set_ticks([0, 0.25, 0.5, 0.75, 1])
color_bar.set_ticklabels([0, 0.25, 0.5, 0.75, 1])

# Show plot
plt.show()

# Close the CGNS file
cgns_file.close()
