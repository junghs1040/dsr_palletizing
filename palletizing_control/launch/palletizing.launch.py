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

def generate_launch_description():
    
    ld = LaunchDescription()
    
    spawn_box_node = Node(package = 'boxes_spawner',
                          executable = 'spawn_boxes',
                          name = 'spawn_boxes',
                          output = 'screen',
                          )
    
    control_node = Node(package = 'palletizing_control',
                          executable = 'palletizing_control',
                          name = 'palletizing_control',
                          output = 'screen',
                          )
    algorithm_node = Node(package = 'palletizing_algorithm',
                          executable = 'palletizing_algorithm',
                          name = 'palletizing_algorithm',
                          output = 'screen',
                          )
                          
    ld.add_action(spawn_box_node)  
    ld.add_action(algorithm_node)  
    ld.add_action(control_node) 
    
    return ld
    

                          
                          
                          
