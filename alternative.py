import numpy as np
from stl import mesh
from mpl_toolkits import mplot3d
import matplotlib.pyplot as plt

# Load the STL file
stl_mesh = mesh.Mesh.from_file('Skull.stl')

# Create a new plot
figure = plt.figure()
axes = mplot3d.Axes3D(figure)

# Add the STL mesh to the plot
axes.add_collection3d(mplot3d.art3d.Poly3DCollection(stl_mesh.vectors))

# Auto-scale the plot
scale = stl_mesh.points.flatten(-1)
axes.auto_scale_xyz(scale, scale, scale)

# Show the plot
plt.show()