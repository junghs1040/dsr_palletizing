import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import ThisLaunchFileDir
from launch.actions import ExecuteProcess
from launch.substitutions import LaunchConfiguration, Command, PythonExpression
from launch.actions import DeclareLaunchArgument
from launch_ros.actions import Node
from launch.substitutions import PathJoinSubstitution
from launch.launch_context import LaunchContext
from launch.conditions import IfCondition

import xacro


# this is the function launch system will look for
def generate_launch_description():

    yaml_file = "boxes_set.yaml"
    package_name = "boxes_spawner"
    world_file_name = "empty.world"

    param_dir = LaunchConfiguration('param_dir',
    default=os.path.join(get_package_share_directory(package_name), "config", yaml_file))
                    
                    
    # create and return launch description object
    return LaunchDescription(
        [
            DeclareLaunchArgument(
                'param_dir',
                default_value = param_dir,
                description = 'Full path of parameter file'),
                
            Node(
                package ='boxes_spawner',
                executable = 'spawn_boxes',
                name = 'spawn_boxes',
                parameters = [param_dir],
                output = 'screen'),

        ]
    )

print("DDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD")
