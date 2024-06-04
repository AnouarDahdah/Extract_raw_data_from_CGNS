import meshio
import numpy as np
import matplotlib.pyplot as plt
mesh=meshio.read("/home/adahdah/dataCADtest10.stl")
points=mesh.points
faces=mesh.cells_dict["triangle"]


points=points-np.min(points)+0.1
points=points/np.max(points)
points=0.95*points
points[:,1]=points[:,1]-np.min(points[:,1])
fig = plt.figure(figsize=plt.figaspect(0.5))
ax = fig.add_subplot(1, 2, 1, projection='3d')
ax.plot_trisurf(points[:,0], points[:,1], points[:,2], triangles=faces, cmap=plt.cm.Spectral)


from pygem.vffd import VFFD,_volume
initvolume=_volume(points,faces)
vffd=VFFD(faces,np.array(initvolume),[2,2,2])

np.random.seed(0)
vffd.array_mu_x=vffd.array_mu_x+0.5*np.random.rand(2,2,2)
vffd.array_mu_y=vffd.array_mu_y+0.5*np.random.rand(2,2,2)
vffd.array_mu_z=vffd.array_mu_z+0.5*np.random.rand(2,2,2)
vffd.adjust_control_points(points)
mesh_def=vffd(points)
mesh_def=mesh_def.reshape(points.shape)
print("Percentage difference from the original mesh is ", np.linalg.norm(mesh_def-points)/np.linalg.norm(points)*100)




