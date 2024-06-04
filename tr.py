import h5py

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Open the CGNS file containing mesh data
cgns_file = h5py.File("/home/adahdah/ID2_Surface15.cgns", "r")

# Define the path to the grid coordinates
grid_coordinates_path = "/Base/Air Body/GridCoordinates"
# Define the path to the interfaces
WSSxPath="/Base/Air Body/Solution00001/meanWSSxMonitor"
WSSyPath="/Base/Air Body/Solution00001/meanWSSyMonitor"
WSSzPath="/Base/Air Body/Solution00001/meanWSSzMonitor"
# Extract grid coordinates from the CGNS file and filter out non-float values
x_dataset = np.array([value for value in cgns_file[grid_coordinates_path + "/CoordinateX/ data"] ])
y_dataset = np.array([value for value in cgns_file[grid_coordinates_path + "/CoordinateY/ data"] ])
z_dataset = np.array([value for value in cgns_file[grid_coordinates_path + "/CoordinateZ/ data"] ])

WSSx=np.array([value for value in cgns_file[WSSxPath + "/ data"] ])
WSSy=np.array([value for value in cgns_file[WSSyPath + "/ data"] ])
WSSz=np.array([value for value in cgns_file[WSSyPath + "/ data"] ])


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


# Create a 3D plot
#fig = plt.figure()
#ax = fig.add_subplot(111, projection='3d')
# Scatter plot of the points
#ax.scatter(x_dataset, y_dataset, z_dataset, c='b', marker='o')

# Optionally set labels
#ax.set_xlabel('X Coordinate')
#ax.set_ylabel('Y Coordinate')
#ax.set_zlabel('Z Coordinate')

# Set title
#ax.set_title('3D Scatter Plot of Mesh Data')

# Show plot
#plt.show()
# Close the CGNS file
cgns_file.close()
