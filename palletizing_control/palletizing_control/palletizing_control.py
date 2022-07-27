import rclpy
import sys
import time 
import signal

import rclpy
import os
import threading, time
import signal
from rclpy.node import Node
from std_srvs.srv import *
from dsr_msgs2.msg import *
from dsr_msgs2.srv import *

sys.dont_write_bytecode = True
sys.path.append( os.path.abspath(os.path.join(os.path.dirname(__file__),"../../../../../common2/bin/common2/imp")) ) # get import pass : DSR_ROBOT2.py 


#--------------------------------------------------------
import DR_init
g_node = None
rclpy.init()
g_node = rclpy.create_node('palletizing_control')
DR_init.__dsr__node = g_node
from DSR_ROBOT2 import *
#--------------------------------------------------------

class SpawnBoxOperator(Node): 
    def __init__(self):
        super().__init__('spawnbox_service_client')
        
        self.spawnbox_service_client = self.create_client(
            SpawnBox, 'spawnbox_operator')
            
    def send_request(self):
        request = SpawnBox.Request()
        request.spawn = True
        futures = self.spawnbox_service_client.call_async(request)
        print("spawn the box!!!")
        return futures
        
        
class GripperOperator(Node):
    def __init__(self):
        super().__init__('vacuum_gripper_controller')
 
        self.gripper_client1 = self.create_client(
            SetBool, '/vacuum_gripper1/switch')
        self.gripper_client2 = self.create_client(
            SetBool, '/vacuum_gripper2/switch')                        
        self.gripper_client3 = self.create_client(
            SetBool, '/vacuum_gripper3/switch')           
        self.gripper_client4 = self.create_client(
            SetBool, '/vacuum_gripper4/switch')
           
         
    def send_gripper_on(self):
        request = SetBool.Request()
        request.data = True
        futures = self.gripper_client1.call_async(request)
        futures = self.gripper_client2.call_async(request)
        futures = self.gripper_client3.call_async(request)
        futures = self.gripper_client4.call_async(request)

        return futures
        
    def send_gripper_off(self):
        request = SetBool.Request()
        request.data = False
        futures = self.gripper_client1.call_async(request)
        futures = self.gripper_client2.call_async(request)
        futures = self.gripper_client3.call_async(request)
        futures = self.gripper_client4.call_async(request)   
        return futures     
        
class GetPalletPos(Node):
    def __init__(self):
    	super().__init__('get_pallet_pos')
    	self.count = 0
    
    	self.pallet_pos_server = self.create_service(
            PalletPos, 'palletizing_pos', self.get_pallet_pos)   
    
    def get_pallet_pos(self, request, response):
        print("get the position info")
        x_pos_ = request.x_pos
        y_pos_ = request.y_pos
        z_pos = request.z_pos
        print(x_pos_)
        print(y_pos_)
        response.success = True
        self.count +=1
        return response
            

def signal_handler(sig, frame):
    print('XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX signal_handler')
    print('XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX signal_handler')
    print('XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX signal_handler')
    global g_node
    publisher = g_node.create_publisher(RobotStop, 'stop', 10)

    msg = RobotStop()
    msg.stop_mode =1 

    publisher.publish(msg)
    #sys.exit(0)
    rclpy.shutdown()


def main(args=None):
    global g_node
    signal.signal(signal.SIGINT, signal_handler)

    spawnbox = SpawnBoxOperator()
    future = spawnbox.send_request()
    
    gripper = GripperOperator()
    pallet_pos = GetPalletPos()

    #----------------------------------------------------------------
    robot = CDsrRobot()
    #----------------------------------------------------------------

    set_velx(100,100)  # set global task speed: 30(mm/sec), 20(deg/sec)
    set_accx(100,100)  # set global task accel: 60(mm/sec2), 40(deg/sec2)
    
    #set_velx(30,20)  # set global task speed: 30(mm/sec), 20(deg/sec)
    #set_accx(60,40)  # set global task accel: 60(mm/sec2), 40(deg/sec2)

    velx=[100, 100]
    accx=[100, 100]

    p2= posj(0.0, 0.0, 90.0, 0.0, 90.0, 0.0) #joint

    x1= posx(400, 500, 800.0, 0.0, 180.0, 0.0) #task
    x2= posx(400, 500, 500.0, 0.0, 180.0, 0.0) #task

    pick_pos = posx(400, 500, 100.0, 0.0, 180.0, 0.0)
    pick_pos_up = posx(400, 500, 500.0, 0.0, 180.0, 0.0)
    pick_pos_r = posx(400, 500, 500.0, 90.0, 180.0, 0.0)
    place_pos = posx(400, -500, 150.0, 0.0, 180.0, 0.0)
    place_pos_up = posx(400, -500, 500.0, 0.0, 180.0, 0.0)
    
    
    while rclpy.ok(): 
     
        # move joint    
        robot.movej(p2, vel=100, acc=100)
        print("------------> movej OK")    
        future2 = gripper.send_gripper_on()
        # move joint task : picking position  
        robot.movel(pick_pos_up, velx, accx)
        print("------------> movel OK")    
        
        # move line : move to pick    
        robot.movel(pick_pos, velx, accx)
        print("------------> movel OK")    
        time.sleep(1)
        
        # picking - if get the true of /grasp picking topic
        # move line : move up
        robot.movel(pick_pos_up, velx, accx)
        print("------------> movel OK")    
        time.sleep(1)        
        
        # move joint task : placing position  
        robot.movel(place_pos_up, velx, accx)
        print("------------> movel OK")    
        time.sleep(1)

        # move line : move to place
        robot.movel(place_pos, velx, accx)
        print("------------> movel OK")    
        time.sleep(1)
        # place
        gripper.send_gripper_off()
        # spawn box
        spawnbox.send_request()
        
        # move line : move up
        robot.movel(place_pos_up, velx, accx)
        print("------------> movel OK")    
        time.sleep(1)   
 

    print('XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX good-bye!')
    print('XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX good-bye!')
    print('XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX good-bye!')

if __name__ == '__main__':
    main()
