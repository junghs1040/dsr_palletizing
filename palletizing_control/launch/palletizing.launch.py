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

args =[
    DeclareLaunchArgument('box_set', default_value = '1', description = 'BOX_SET_NUM' ),
]

def generate_launch_description():
    
    spawn_box_node = Node(package = 'boxes_spawner',
                          executable = 'spawn_boxes',
                          name = 'spawn_boxes',
                          output = 'screen',
                          )
    
    control_node = Node(package = 'palletizing_control',
                          executable = 'palletizing_control',
                          name = 'palletizing_control',
                          output = 'screen',
                          parameters = [ 
                                        {"box_set" : LaunchConfiguration('box_set') }, 
                                       ]
                          )

    return LaunchDescription(args + [
        spawn_box_node,
        control_node,
        ])

                          
                          
                          
