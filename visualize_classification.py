import argparse
import json
import os
import open3d as o3d
import numpy as np

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Classify points of a point cloud')
    parser.add_argument('cloud', type=str,
                        help='Path to the input point cloud.')
    parser.add_argument('--data_path', default=None, type=str,
                        help='Path to classification file. Default is "path/to/cloud.ply.json".')
    args = parser.parse_args()
    
    # set default path if necessary
    if args.data_path is None:
        data_path = args.cloud + ".json"
    else:
        data_path = args.data_path
    
    # load data
    if os.path.isfile(data_path):
        with open(data_path, "r") as data_object:
            data = json.load(data_object)
        print("Data loaded from: {}".format(data_path))
    else:
        raise FileNotFoundError(data_path)

    # load cloud
    cloud = o3d.io.read_point_cloud(args.cloud)
    
    # set colors based on label
    cloud_colors = np.asarray(cloud.colors)
    cloud_colors[:, :] = 0.0
    colors = np.random.rand(10, 3)
    for key, value in data.items():
        cloud_colors[int(key), :] = colors[value, :]
    cloud.colors = o3d.utility.Vector3dVector(cloud_colors)

    # show
    o3d.visualization.draw_geometries([cloud])