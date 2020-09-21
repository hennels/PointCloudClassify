# PointCloudClassify
A simple point classification (point cloud segmentation) interface for data collection built on top of Open3D. This project was built to be an extremely simple but usable interface for collecting point cloud segmentation ground truth data.

## Installation
Since this is a very simple project it requires little to no installation. If you manage python packages in some way on your own, just install the packages listed in the **Dependancies** section. If you want an installation that is known to work, use the **Virtual Environments** section instead. I reccomend using virtual environments if you are not already, they make life so much easier in the long run.

### Dependancies
This project requires only `numpy` and `open3d`. 

### Virtual Environments
Currently this project uses [Pipenv](https://pipenv-fork.readthedocs.io) for virtual environment managment. If you have Pipenv installed in your system you should be able to get a working installation of this project by simply running the following command from the root folder of this project:
```
pipenv install
```
If you want to add the files for a different virtual environment managment system like Poetry or Conda, feel free to do so. 

## Usage
There are currently two seprate scripts provided in this porject: `classify.py` for collecting data and `visualize_classification.py` for visualizing the result. Both scripts use argparse and should give usage information if run with a `-h` or `--help` parameter.

Example usage:
```
python classify.py path/to/cloud.ply
```
or if you are using pipenv
```
pipenv run python classify.py path/to/cloud.ply
```

