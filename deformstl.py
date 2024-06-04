import matplotlib 
import numpy as np

from pygem import FFD
from smithers import io

def plot(data, color=None):

    from mpl_toolkits.mplot3d import Axes3D
    from mpl_toolkits.mplot3d.art3d import Poly3DCollection
    import matplotlib.pyplot as plt

    if color is None:
        color = (0, 0, 1, 0.1)
    fig = plt.figure(figsize=(16,10))

    verts = [data['points'][cell] for cell in data['cells']]
    ax = fig.add_subplot(111, projection='3d')
    faces = Poly3DCollection(verts, linewidths=1, edgecolors='k')
    faces.set_facecolor(color)
    
    ax.add_collection3d(faces)
    ax.set_xlim3d(-.8, .8)
    ax.set_ylim3d(-.8, .8)
    ax.set_zlim3d(-.8, .8)
    ax.set_aspect('equal','box')

    plt.show()

stl_filename = "/home/adahdah/dataCADtest10"

stl_content = io.STLHandler.read(stl_filename)
stl_content['points'] = ffd(stl_content['points'])
io.STLHandler.write('deform_cube.stl', stl_content)