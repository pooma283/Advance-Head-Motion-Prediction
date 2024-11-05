
import numpy as np
from datatools.visualization import AttentionMap
from datatools.generator import pointcloud_cube

if __name__ == '__main__':
    data = np.loadtxt(open(
        '', "rb"), delimiter=",", skiprows=1)
    am = AttentionMap()
    am.draw(data, pointcloud_cube(-5.0, 5.0, 1.0),
            title='User Attention (Normalized)')