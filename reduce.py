import pandas as pd
import numpy as np
from sklearn.decomposition import PCA
from sklearn.cluster import MiniBatchKMeans
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Load the CSV file
data = pd.read_csv('/home/adahdah/coordinate_datad20.csv')

# Convert to numpy array
points = data[['X', 'Y', 'Z']].to_numpy()

# Apply PCA to reduce dimensions from 3D to 2D
pca = PCA(n_components=3)
points_2d = pca.fit_transform(points)

# Set the desired number of points
num_points = 10000  # Adjust this number as needed

# Apply MiniBatchKMeans clustering to downsample the points
kmeans = MiniBatchKMeans(n_clusters=num_points, batch_size=10000)
kmeans.fit(points_2d)
cluster_centers_2d = kmeans.cluster_centers_

# Map the 2D cluster centers back to the original 3D space
inverse_transform = pca.inverse_transform(cluster_centers_2d)

# Convert the reduced points back to DataFrame
downsampled_df = pd.DataFrame(inverse_transform, columns=['X', 'Y', 'Z'])

# Save the downsampled data to a new CSV file
downsampled_df.to_csv('coordinate_datad20.csv', index=False)

# Optional: Plotting the results in 3D
fig = plt.figure(figsize=(8, 6))
ax = fig.add_subplot(111, projection='3d')
ax.scatter(downsampled_df['X'], downsampled_df['Y'], downsampled_df['Z'], s=2)
ax.set_title("PCA + MiniBatchKMeans downsampled car shape")
ax.set_xlabel("X")
ax.set_ylabel("Y")
ax.set_zlabel("Z")
plt.show()

print("PCA and MiniBatchKMeans downsampling complete. The reduced data has been saved to 'coordinate_datad20.csv'.")
