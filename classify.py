import argparse
import json
import os
import random
from functools import partial
import open3d as o3d
import numpy as np

HELP_MESSAGE = """
classify.py window keyboard controls:
  Q: Quit
  A: Make the currently selected point bigger.
  Z: Make the currently selected point smaller.
  C: Center the camera view on the currently selected point.
  U: Undo last classification (lets you reclassify the previous point).
  S: Show statistics. Prints class counts.
  Spacebar: skip this point (does not add a label for this point).
  0: Classify point as class 0.
  1: Classify point as class 1.
  2: Classify point as class 2.
  3: Classify point as class 3.
  4: Classify point as class 4.
  5: Classify point as class 5.
  6: Classify point as class 6.
  7: Classify point as class 7.
  8: Classify point as class 8.
  9: Classify point as class 9.
"""

SELECTED_POINT_COLORS = {
    'red':[1.0, 0.0, 0.0],
    'green':[0.0, 1.0, 0.0],
    'blue':[0.0, 0.0, 1.0]
}

class PointClassRecorder:
    def __init__(self, cloud_path, data_path, starting_radius=0.25, selected_point_color='red'):
        self.pcd = o3d.io.read_point_cloud(cloud_path)
        if os.path.isfile(data_path):
            with open(data_path, "r") as data_object:
                self.data = json.load(data_object)
            print("Data loaded from: {}".format(data_path))
        else:
            self.data = {}
            print("New data structure created.")
        if self.pcd.has_points():
            self.points = np.asarray(self.pcd.points)
            self.N = self.points.shape[0]
            if self.N < 1:
                raise ValueError("Cloud cannot be empty")
        self.sphere = o3d.geometry.TriangleMesh.create_sphere(radius=starting_radius)
        self.sphere.compute_vertex_normals()
        self.sphere.paint_uniform_color(SELECTED_POINT_COLORS[selected_point_color])
        self.current = self.random_point()
        self.sphere.translate(self.points[self.current, :])
        self.callbacks = {}
        for i in range(10):
            self.callbacks[ord(str(i))] = partial(self.record_point, i)
        self.callbacks[ord('A')] = self.scale_up
        self.callbacks[ord('Z')] = self.scale_down
        self.callbacks[ord('C')] = self.center_on_current
        self.callbacks[ord('U')] = self.undo_point
        self.callbacks[ord('S')] = self.print_stats
        self.callbacks[ord(' ')] = self.next_point
        print(HELP_MESSAGE)
        o3d.visualization.draw_geometries_with_key_callbacks([self.pcd, self.sphere], self.callbacks)
        with open(data_path, "w") as data_file:
            json.dump(self.data, data_file)
        print("Data written to: {}".format(data_path))
    
    def center_on_current(self, vis):
        vis.get_view_control().set_lookat(self.points[self.current, :])
        return False

    def random_point(self):
        self.current = random.randint(0, self.N)
        while str(self.current) in self.data:
            self.current = random.randint(0, self.N)
        return self.current
    
    def next_point(self, vis):
        self.sphere.translate(-1*self.points[self.current, :])
        self.random_point()
        self.sphere.translate(self.points[self.current, :])
        self.center_on_current(vis)
        return True
    
    def record_point(self, class_number, vis):
        self.data[str(self.current)] = class_number
        self.next_point(vis)
        return True

    def undo_point(self, vis):
        try:
            prev_current, _ = self.data.popitem()
            self.sphere.translate(-1*self.points[self.current, :])
            self.current = int(prev_current)
            self.sphere.translate(self.points[self.current, :])
            self.center_on_current(vis)
        except KeyError:
            print("No actions to undo")
        except:
            raise
        return True

    def scale_up(self, vis):
        self.sphere.scale(1.1, center=self.points[self.current, :])
        return True
    
    def scale_down(self, vis):
        self.sphere.scale(0.9, center=self.points[self.current, :])
        return True
    
    def print_stats(self, vis):
        stats = np.zeros(10, dtype=int)
        for k, v in self.data.items():
            stats[v] = stats[v] + 1
        print("Counts for each class are:")
        for index in range(stats.shape[0]):
            if stats[index] > 0:
                print("    Class {}: {}".format(index, stats[index]))
        print("Done")
        return False

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Classify points of a point cloud')
    parser.add_argument('cloud', type=str,
                        help='Path to the input point cloud.')
    parser.add_argument('--radius', default=0.25, type=float,
                        help='Intial radius of selected point which can be adjusted later (float).')
    parser.add_argument('--color', default='red', type=str,
                        help='Intial color of selected point. Choices are: {}'.format(list(SELECTED_POINT_COLORS.keys())))
    parser.add_argument('--output_path', default=None, type=str,
                        help='Path to output file. Default is "path/to/cloud.ply.json".')
    args = parser.parse_args()
    
    if args.output_path is None:
        recorder = PointClassRecorder(args.cloud,
                                      args.cloud+".json",
                                      starting_radius=args.radius,
                                      selected_point_color=args.color)
    else:
        recorder = PointClassRecorder(args.cloud,
                                      args.output_path,
                                      starting_radius=args.radius,
                                      selected_point_color=args.color)