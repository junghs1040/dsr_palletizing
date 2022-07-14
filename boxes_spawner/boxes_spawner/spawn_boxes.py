import os
import sys
import rclpy
import time
from ament_index_python.packages import get_package_share_directory
from gazebo_msgs.srv import SpawnEntity

def boxes_choice(urdf_file_path, box_num):
    # Set data for request
    request = SpawnEntity.Request()
    request.name = str(box_num)
    request.xml = open(urdf_file_path, 'r').read()
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
    box_num = 4
    package_name = "boxes_spwaner"
    robot_file = "box1.urdf"
    world_file_name = "empty.world"
    
    node.get_logger().info(
        'Creating Service client to connect to `/spawn_entity`')
    client = node.create_client(SpawnEntity, "/spawn_entity")

    node.get_logger().info("Connecting to `/spawn_entity` service...")
    if not client.service_is_ready():
        client.wait_for_service()
        node.get_logger().info("...connected!")

    # Get path to the turtlebot3 burgerbot
    urdf_file_path = os.path.join(
        get_package_share_directory(package_name), "urdf", robot_file)
        
    for i in range(box_num):
        req = boxes_choice(urdf_file_path, i)
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
    
