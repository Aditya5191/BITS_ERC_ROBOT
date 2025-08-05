from launch import LaunchDescription
import os
import xacro
from ament_index_python.packages import get_package_share_directory
from launch.actions import ExecuteProcess
from launch_ros.actions import Node
from launch.substitutions import Command, FindExecutable, PathJoinSubstitution
from launch_ros.substitutions import FindPackageShare

def generate_launch_description():

    namePackage = "Gazebo_world"
    modelFileReativePath='urdf/forklift/robot.urdf.xacro'

    # Path to find xacro file
    xacro_file = PathJoinSubstitution([
        FindPackageShare("Gazebo_world"),
        "urdf",
        "forklift",
        "robot.urdf.xacro"
    ])

    # Use xacro to generate robot description
    # robot_description = Command([
    #     FindExecutable(name="xacro"),
    #     xacro_file
    # ])
    pathModelFile = os.path.join(get_package_share_directory(namePackage),modelFileReativePath)
    robot_description = xacro.process_file(pathModelFile).toxml()

    return LaunchDescription([

        # Robot state publisher
        Node(
            package="robot_state_publisher",
            executable="robot_state_publisher",
            parameters=[{"robot_description":robot_description}],
            output="screen"
        ),

        # Joint state publisher GUI
        Node(
            package="joint_state_publisher_gui",
            executable="joint_state_publisher_gui",
            output="screen"
        ),

        Node(
            package="rviz2",
            executable="rviz2",
            name="rviz2",
            output="screen",
            arguments=["-d", PathJoinSubstitution([
                FindPackageShare("Gazebo_world"),
                'forklift_config.rviz'
            ])]
        )
    ])