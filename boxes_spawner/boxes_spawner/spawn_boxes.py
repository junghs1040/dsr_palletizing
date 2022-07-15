import os
import sys
import rclpy
import time
import yaml
from ament_index_python.packages import get_package_share_directory
from gazebo_msgs.srv import SpawnEntity

def yaml_read(configParams,n):
    width = configParams['box_set1']['box'+str(n)][0]
    length = configParams['box_set1']['box'+str(n)][1]
    height = configParams['box_set1']['box'+str(n)][2]
    return width, length, height

def boxes_choice(urdf_file_path, box_num, width, length, height):
    # Set data for request
    
    request = SpawnEntity.Request()
    request.name = str(box_num)
    request.xml = "<?xml version=\"1.0\" ?><robot name=\"box1\"><link name=\"box1\"><visual><origin xyz=\"0 0 0\" rpy=\"0 0 0\"/><geometry><box size=\""+str(width)+" "+str(length)+" "+str(height)+"\"/></geometry></visual><inertial><origin xyz=\"0 0 0\" rpy=\"0 0 0\"/><mass value=\"1\"/><inertia ixx=\"100\" ixy=\"0.0\" ixz=\"0.0\" iyy=\"100\" iyz=\"0.0\" izz=\"100\"/></inertial><collision><origin xyz=\"0 0 0\" rpy=\"0 0 0\"/><geometry><box size=\""+str(width)+" "+str(length)+" "+str(height)+"\"/></geometry></collision></link></robot>"
    #request.robot_namespace = argv[1]
    request.initial_pose.position.x = float(0.0)
    request.initial_pose.position.y = float(0.0)
    request.initial_pose.position.z = float(1.0)    
    
    return request

def main():
    """ Main for spawning boxes"""
    # Get input arguments from user
    argv = sys.argv[1:]

    # Start node
    rclpy.init()
    node = rclpy.create_node("spawn_boxes") 
    box_num = 5
    package_name = "boxes_spawner"
    robot_file = "box1.urdf"
    yaml_file = "boxes_set.yaml"
    world_file_name = "empty.world"
    
    node.get_logger().info(
        'Creating Service client to connect to `/spawn_entity`')
    client = node.create_client(SpawnEntity, "/spawn_entity")
    node.get_logger().info("Connecting to `/spawn_entity` service...")
    if not client.service_is_ready():
        client.wait_for_service()
        node.get_logger().info("...connected!")

    # Get path to the box urdf
    urdf_file_path = os.path.join(
        get_package_share_directory(package_name), "urdf", robot_file)
    
    # Get the yaml configuration
    yaml_file_path = os.path.join(
        get_package_share_directory(package_name), "config", yaml_file)
    yaml_config = open(yaml_file_path, 'r').read()
    configParams = yaml.safe_load(yaml_config)

    print(configParams['box_set1'])
        
    for i in range(box_num):
        width, length, height = yaml_read(configParams,i+1)
        req = boxes_choice(urdf_file_path, i, width, length, height)
        node.get_logger().info("Sending service request to `/spawn_entity`")
        future = client.call_async(req)
        time.sleep(1)
        rclpy.spin_until_future_complete(node, future)
        if future.result() is not None:
            print('response: %r' % future.result())
        else:
            raise RuntimeError(
             'exception while calling service: %r' % future.exception())

    node.get_logger().info("Done! Shutting down node.")
    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()
    
