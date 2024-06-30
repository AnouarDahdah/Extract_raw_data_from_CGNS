import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Step 1: Read data from the first CSV file
df1 = pd.read_csv('/home/adahdah/coordinate_datad7.csv')

# Step 2: Read data from the second CSV file
df2 = pd.read_csv('/home/adahdah/coordinate_datad20.csv')

# Step 3: Create a 3D scatter plot
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')

# Plot data from the first CSV
ax.scatter(df1['X'], df1['Y'], df1['Z'], c='blue', s=5, label='Design 1')

# Plot data from the second CSV
ax.scatter(df2['X'], df2['Y'], df2['Z'], c='red', s=5, label='Design 2')

# Step 4: Update layout
ax.set_title('3D Scatter Plot Comparison of Two Designs')
ax.set_xlabel('X Axis')
ax.set_ylabel('Y Axis')
ax.set_zlabel('Z Axis')
ax.legend()

# Step 5: Save the plot as an image file
plt.savefig('comparison_plot.png')

# Optional: Show the plot in an interactive window
plt.show()

print("The 3D scatter plot comparison has been saved to 'comparison_plot.png'.")
