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


# this is the function launch  system will look for
def generate_launch_description():
    use_sim_time = LaunchConfiguration('use_sim_time', default='false')

    robot_file = "box1.urdf"
    package_name = "boxes_spwaner"
    world_file_name = "empty.world"

    # full  path to urdf and world file
    world = os.path.join(
        get_package_share_directory(package_name), "worlds", world_file_name
    )
    urdf = os.path.join(get_package_share_directory(package_name), "urdf", robot_file)


    # read urdf contents because to spawn an entity in
    # gazebo we need to provide entire urdf as string on  command line
    robot_desc = open(urdf, "r").read()

    # double quotes need to be with escape sequence
    xml = robot_desc.replace('"', '\\"')

    # this is argument format for spwan_entity service
    spwan_args = '{name: "box1", xml: "' + xml + '" }'

    robot_state_publisher_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[{'use_sim_time': use_sim_time, 'robot_description': robot_desc}],
        arguments=[urdf],
    )


    # create and return launch description object
    return LaunchDescription(
        [
            # robot state publisher allows robot model spawn in RVIZ
            robot_state_publisher_node,
            # start gazebo, notice we are using libgazebo_ros_factory.so instead of libgazebo_ros_init.so
            # That is because only libgazebo_ros_factory.so contains the service call to /spawn_entity
            #ExecuteProcess(
           #     cmd=["gazebo", "--verbose", world, "-s", "libgazebo_ros_factory.so"],
            #    output="screen",
          #  ),
            # tell gazebo to spwan your robot in the world by calling service
            ExecuteProcess(
                cmd=[ "ros2", "service", "call", "/spawn_entity", "gazebo_msgs/SpawnEntity", spwan_args ],
                output="screen",
            ),
        ]
    )
