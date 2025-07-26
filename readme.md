# Gazebo World Package

This ROS2 package contains custom Gazebo models and world files.

## Contents

### Models
The `src/Gazebo_world/models/` directory contains various models including:
- Bookshelf
- Multiple cardboard boxes
- Other custom models

### Worlds
World files are located in the `src/Gazebo_world/worlds/` directory.

## Usage

Before running Gazebo, you need to set the GAZEBO_MODEL_PATH environment variable so Gazebo can locate the custom models:

```bash
echo 'export GZ_SIM_RESOURCE_PATH="<path_to_your_models>:$GZ_SIM_RESOURCE_PATH"' >> ~/.bashrc
```
```bash
source ~/.bashrc

```
# To Test the world

```bash
cd src/Gazebo_world/worlds
```
```bash
gz sim world_fixed.sdf
```
- Note : You will see errors related to some pngs not loaded.. but they are atually loaded and are visible in the simulation. If you cant see the simulation then the model resource path you set is wrong. you can ignore the errors for png not loaded.

## Building

To build this package:

```bash
colcon build --packages-select Gazebo_world
```
## TO DO
- make a launch file
- make Robot 