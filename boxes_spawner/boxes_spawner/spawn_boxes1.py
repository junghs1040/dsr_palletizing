import os
import sys
import rclpy
import time
import yaml
from rclpy.node import Node
from ament_index_python.packages import get_package_share_directory
from gazebo_msgs.srv import SpawnEntity
from dsr_msgs2.msg import *
from dsr_msgs2.srv import *

class SpawnBoxServer(Node):
    def __init__(self):
        super().__init__('spawnbox_service_server')
        
        self.spawnbox_service_server = self.create_service(
            SpawnBox, 'spawnbox_operator', self.spawn_box)
            
    def spawn_box(self, request, response):
        self.req = request.spawn
        width, length, height = boxes_data_read()
        #response.width = width
        #response.length = length
        #response.height = height
        print("hello")
        spawn_box = 1
        no_spawn_box = 0
        if req == True:
            return spawn_box
        else:
            return no_spawn_box


    def yaml_read(configParams,n):
        width = configParams['box_set1']['box'+str(n)][0]
        length = configParams['box_set1']['box'+str(n)][1]
        height = configParams['box_set1']['box'+str(n)][2]
        return width, length, height

    def boxes_choice(box_num, width, length, height):
        # Set data for request
        mass = 0.005
        #ixx = mass*(length*length+height*height)/12
        #iyy = mass*(width*width+height*height)/12
        #izz = mass*(length*length+width*width)/12
        ixx = 0.001
        iyy = 0.001
        izz = 0.001
        request = SpawnEntity.Request()
        request.name = str(box_num)
        request.xml = "<?xml version=\"1.0\" ?><robot name=\"box1\"><link name=\"box1\"><visual><origin xyz=\"0 0 0\" rpy=\"0 0 0\"/><geometry><box size=\""+str(width)+" "+str(length)+" "+str(height)+"\"/></geometry></visual><inertial><origin xyz=\"0 0 0\" rpy=\"0 0 0\"/><mass value=\""+str(mass)+"\"/><inertia ixx=\""+str(ixx)+"\" ixy=\"0.0\" ixz=\"0.0\" iyy=\""+str(iyy)+"\" iyz=\"0.0\" izz=\""+str(izz)+"\"/></inertial><collision><origin xyz=\"0 0 0\" rpy=\"0 0 0\"/><geometry><box size=\""+str(width)+" "+str(length)+" "+str(height)+"\"/></geometry></collision></link><gazebo reference=\"box1\"><material>Gazebo/Red</material></gazebo></robot>"
        #request.robot_namespace = argv[1]
        request.initial_pose.position.x = float(0.4)
        request.initial_pose.position.y = float(0.5)
        request.initial_pose.position.z = float(0.0)    
    
        return request

    def boxes_data_read():
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
    
        # Get the yaml configuration
        yaml_file_path = os.path.join(
        get_package_share_directory(package_name), "config", yaml_file)
        yaml_config = open(yaml_file_path, 'r').read()
        configParams = yaml.safe_load(yaml_config)   

def main():

    argv = sys.argv[1:]
    rclpy.init()
    node = rclpy.create_node("spawn_boxes") 
    
    spawn_box = SpawnBoxServer()
    
    node.get_logger().info(
        'Creating Service client to connect to `/spawn_entity`')
    client = node.create_client(SpawnEntity, "/spawn_entity")
    node.get_logger().info("Connecting to `/spawn_entity` service...")
    if not client.service_is_ready():
        client.wait_for_service()
        node.get_logger().info("...connected!")

    
    # Get the yaml configuration
    yaml_file_path = os.path.join(
        get_package_share_directory(package_name), "config", yaml_file)
    yaml_config = open(yaml_file_path, 'r').read()
    configParams = yaml.safe_load(yaml_config)

    rclpy.spin(spawn_box)


    node.get_logger().info("Done! Shutting down node.")
    rclpy.shutdown()


if __name__ == "__main__":
    main()
    
