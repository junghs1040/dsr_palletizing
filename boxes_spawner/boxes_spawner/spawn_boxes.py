import os
import sys
import rclpy
import time
import yaml
from rclpy.node import Node
from dsr_msgs2.msg import *
from dsr_msgs2.srv import *
from ament_index_python.packages import get_package_share_directory
from gazebo_msgs.srv import SpawnEntity

class SpawnBoxServer(Node):
    def __init__(self):
        super().__init__('spawn_boxes')
        
        self.spawnbox_service_server = self.create_service(
            SpawnBox, 'spawnbox_operator', self.spawn_box)
        self.client = self.create_client(SpawnEntity, "/spawn_entity")        
    count = 0     
    def spawn_box(self, request, response):
        req = request.spawn
        num = 0
        width = float(request.box_info[0])/1000
        length = float(request.box_info[1])/1000
        height = float(request.box_info[2])/1000
        #width, length, height = self.boxes_data_read(self.count)
        response.width = width
        response.length = length
        response.height = height
        print(self.count)
        
        req = self.boxes_choice(self.count+1,width,length,height)        
        future = self.client.call_async(req)
        if num == 0:
            req = self.pallet_make() 
            future = self.client.call_async(req)
            num += 1
        self.count +=1
        return response

    

    def yaml_read(self, configParams,n):
        width = configParams['box_set1']['box'+str(n)][0]
        length = configParams['box_set1']['box'+str(n)][1]
        height = configParams['box_set1']['box'+str(n)][2]
        return width, length, height

    def boxes_choice(self, box_num, width, length, height):
        # Set data for request
        mass = 0.005
        #ixx = mass*(length*length+height*height)/12
        #iyy = mass*(width*width+height*height)/12
        #izz = mass*(length*length+width*width)/12
        #ixx = 0.001
        #iyy = 0.001
        #izz = 0.001
        ixx = 100
        iyy = 100
        izz = 100
        request = SpawnEntity.Request()
        request.name = str(box_num)
        request.xml = "<?xml version=\"1.0\" ?><robot name=\"box1\"><link name=\"box1\"><visual><origin xyz=\"0 0 0\" rpy=\"0 0 0\"/><geometry><box size=\""+str(width)+" "+str(length)+" "+str(height)+"\"/></geometry></visual><inertial><origin xyz=\"0 0 0\" rpy=\"0 0 0\"/><mass value=\""+str(mass)+"\"/><inertia ixx=\""+str(ixx)+"\" ixy=\"0.0\" ixz=\"0.0\" iyy=\""+str(iyy)+"\" iyz=\"0.0\" izz=\""+str(izz)+"\"/></inertial><collision><origin xyz=\"0 0 0\" rpy=\"0 0 0\"/><geometry><box size=\""+str(width)+" "+str(length)+" "+str(height)+"\"/></geometry></collision></link><gazebo reference=\"box1\"><material>Gazebo/Red</material></gazebo></robot>"
        #request.robot_namespace = argv[1]
        request.initial_pose.position.x = float(0.4)
        request.initial_pose.position.y = float(0.5)
        request.initial_pose.position.z = float(0.0)        
        return request
        
    def pallet_make(self):
        # Set data for request
        mass = 0.005
        #ixx = mass*(length*length+height*height)/12
        #iyy = mass*(width*width+height*height)/12
        #izz = mass*(length*length+width*width)/12
        width = 0.5
        length = 0.5
        height = 0.05
        ixx = 100
        iyy = 100
        izz = 100
        request = SpawnEntity.Request()
        request.name = "pallet"
        request.xml = "<?xml version=\"1.0\" ?><robot name=\"box1\"><link name=\"box1\"><visual><origin xyz=\"0 0 0\" rpy=\"0 0 0\"/><geometry><box size=\""+str(width)+" "+str(length)+" "+str(height)+"\"/></geometry></visual><inertial><origin xyz=\"0 0 0\" rpy=\"0 0 0\"/><mass value=\""+str(mass)+"\"/><inertia ixx=\""+str(ixx)+"\" ixy=\"0.0\" ixz=\"0.0\" iyy=\""+str(iyy)+"\" iyz=\"0.0\" izz=\""+str(izz)+"\"/></inertial><collision><origin xyz=\"0 0 0\" rpy=\"0 0 0\"/><geometry><box size=\""+str(width)+" "+str(length)+" "+str(height)+"\"/></geometry></collision></link><gazebo reference=\"box1\"><material>Gazebo/Black</material></gazebo></robot>"
        request.initial_pose.position.x = float(0.4)
        request.initial_pose.position.y = float(-0.5)
        request.initial_pose.position.z = float(0.0)        
        return request

    def boxes_data_read(self, count):
        i = count
        package_name = "boxes_spawner"
        robot_file = "box1.urdf"
        yaml_file = "boxes_set.yaml"
        world_file_name = "empty.world"
        
    
        # Get the yaml configuration
        yaml_file_path = os.path.join(
        get_package_share_directory(package_name), "config", yaml_file)
        yaml_config = open(yaml_file_path, 'r').read()
        configParams = yaml.safe_load(yaml_config)   
        width, length, height = self.yaml_read(configParams,i+1)
        
        return width, length, height

def main():

    argv = sys.argv[1:]
    rclpy.init()
    # node = rclpy.create_node("spawn_boxes") 
    
    spawn_box = SpawnBoxServer()
    rclpy.spin(spawn_box)


    node.get_logger().info("Done! Shutting down node.")
    rclpy.shutdown()


if __name__ == "__main__":
    main()
    
