import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription, TimerAction
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare
import xacro

def generate_launch_description():
    # Declare launch arguments for spawn position
    declare_use_sim_time = DeclareLaunchArgument(
        'use_sim_time',
        default_value='true',
        description='Use simulation (Gazebo) clock if true'
    )
    
    declare_robot_name = DeclareLaunchArgument(
        'robot_name',
        default_value='forklift',
        description='Name of the robot'
    )
    
    declare_robot_namespace = DeclareLaunchArgument(
        'robot_namespace',
        default_value='',
        description='Namespace for the robot'
    )
    
    declare_x_spawn = DeclareLaunchArgument(
        'x_spawn',
        default_value='0.0',
        description='X position to spawn the robot'
    )
    
    declare_y_spawn = DeclareLaunchArgument(
        'y_spawn',
        default_value='-3.0',
        description='Y position to spawn the robot'
    )
    
    declare_z_spawn = DeclareLaunchArgument(
        'z_spawn',
        default_value='0.0',
        description='Z position to spawn the robot'
    )
    
    declare_roll_spawn = DeclareLaunchArgument(
        'roll_spawn',
        default_value='0.0',
        description='Roll orientation to spawn the robot'
    )
    
    declare_pitch_spawn = DeclareLaunchArgument(
        'pitch_spawn',
        default_value='0.0',
        description='Pitch orientation to spawn the robot'
    )
    
    declare_yaw_spawn = DeclareLaunchArgument(
        'yaw_spawn',
        default_value='0.0',
        description='Yaw orientation to spawn the robot'
    )
    
    declare_world_file = DeclareLaunchArgument(
        'world_file',
        default_value='worlds/world_fixed.sdf',
        description='Path to the world file'
    )

    # Get package share directory
    pkg_share = get_package_share_directory('Gazebo_world')
    
    # Get the path to the URDF file
    urdf_file = os.path.join(pkg_share, 'urdf', 'robot.xacro')
    
    # Process the URDF file properly using xacro directly
    # This is CRITICAL - using xacro.process_file() ensures the robot description is properly generated
    robot_description_config = xacro.process_file(urdf_file)
    robot_description = robot_description_config.toxml()
    
    # Robot state publisher - must be started FIRST
    # This publishes the robot description that both Gazebo and RViz need
    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        namespace=LaunchConfiguration('robot_namespace'),
        parameters=[{
            'robot_description': robot_description,
            'use_sim_time': LaunchConfiguration('use_sim_time')
        }],
        output='screen'
    )
    
    # Create the entity spawner node
    # This will be delayed to ensure Gazebo is ready
    spawn_entity = Node(
        package='ros_gz_sim',
        executable='create',
        arguments=[
            '-name', LaunchConfiguration('robot_name'),
            '-namespace', LaunchConfiguration('robot_namespace'),
            '-topic', 'robot_description',
            '-x', LaunchConfiguration('x_spawn'),
            '-y', LaunchConfiguration('y_spawn'),
            '-z', LaunchConfiguration('z_spawn'),
            '-R', LaunchConfiguration('roll_spawn'),
            '-P', LaunchConfiguration('pitch_spawn'),
            '-Y', LaunchConfiguration('yaw_spawn')
        ],
        output='screen'
    )
    
    # RViz node
    rviz_node = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        output='screen',
        arguments=['-d', os.path.join(pkg_share, 'forklift_config.rviz')]
    )
    
    # Create timers for proper startup sequence
    # Gazebo needs time to initialize before we spawn the robot
    delayed_spawn_entity = TimerAction(
        period=5.0,  # Wait 5 seconds for Gazebo to initialize
        actions=[spawn_entity]
    )
    
    # RViz needs to start after the robot is spawned and TF tree is populated
    delayed_rviz = TimerAction(
        period=7.0,  # Wait 7 seconds total (2 seconds after spawn)
        actions=[rviz_node]
    )
    
    # Create launch description
    ld = LaunchDescription()
    
    # Add launch arguments
    ld.add_action(declare_use_sim_time)
    ld.add_action(declare_robot_name)
    ld.add_action(declare_robot_namespace)
    ld.add_action(declare_x_spawn)
    ld.add_action(declare_y_spawn)
    ld.add_action(declare_z_spawn)
    ld.add_action(declare_roll_spawn)
    ld.add_action(declare_pitch_spawn)
    ld.add_action(declare_yaw_spawn)
    ld.add_action(declare_world_file)
    
    # Add robot_state_publisher first - critical for proper initialization
    ld.add_action(robot_state_publisher)
    
    # Launch Gazebo
    world_file_path = PathJoinSubstitution([
        FindPackageShare('Gazebo_world'),
        LaunchConfiguration('world_file')
    ])
    
    gazebo_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            os.path.join(
                get_package_share_directory('ros_gz_sim'),
                'launch',
                'gz_sim.launch.py'
            )
        ]),
        launch_arguments={
            'gz_args': ['-r -v 4 ', world_file_path],
            'on_exit_shutdown': 'true'
        }.items()
    )

    bridge_params = os.path.join(
    get_package_share_directory("Gazebo_world"),
    'launch',
    'bridge_params.yaml'
    )

    start_gazebo_ros_bridge_cmd = Node(
    package='ros_gz_bridge',
    executable='parameter_bridge',
    name='parameter_bridge',
    output='screen',
    arguments=[
        '--ros-args',
        '-p',
        f'config_file:={bridge_params}',
        ],
    )

    ld.add_action(gazebo_launch)
    
    # Add delayed actions
    ld.add_action(delayed_spawn_entity)
    ld.add_action(delayed_rviz)
    ld.add_action(start_gazebo_ros_bridge_cmd)
    
    return ld