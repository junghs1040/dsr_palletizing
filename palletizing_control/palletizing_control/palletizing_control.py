
import sys
import time 
import rclpy
import os
import threading, time
import signal

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

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
        
class Algorithm(Node):
    def __init__(self):

        super().__init__('palletizing_algorithm') 
        
        self.declare_parameter('box_set',1)
        self.param_box = self.get_parameter('box_set')
        self.get_logger().info("box_set :%s" %(str(self.param_box.value)))
        self.cum_x = 0
        self.cum_y = 0
        self.box_set1 = [[0.115, 0.1, 0.075],[0.16, 0.125, 0.075],[0.1, 0.075, 0.075],[0.195, 0.16, 0.075],[0.15, 0.1, 0.075],[0.15, 0.1, 0.075],[0.16, 0.125, 0.075],
                         [0.15,0.15,0.15],[0.1,0.1,0.075],[0.195,0.16,0.15],[0.135,0.075,0.075],[0.16,0.125,0.075],[0.15,0.1,0.075],
                         [0.195,0.16,0.15],[0.195,0.16,0.075],[0.15,0.15,0.15],[0.135,0.075,0.075],[0.15,0.15,0.15],[0.135,0.075,0.075],[0.115,0.1,0.075]]

        self.box_set2 = [[0.160, 0.125, 0.075],[0.195, 0.160, 0.150],[0.115, 0.100, 0.075],[0.100, 0.100, 0.075],[0.195, 0.160, 0.150],[0.135, 0.075, 0.075],
                         [0.150, 0.100, 0.075],[0.075, 0.075, 0.075],[0.100, 0.100, 0.075],[0.195, 0.160, 0.150],[0.135, 0.075, 0.075],[0.160, 0.125, 0.075],
                         [0.150, 0.100, 0.075],[0.195, 0.160, 0.150],[0.195, 0.160, 0.075],[0.150, 0.150, 0.150],[0.135, 0.075, 0.075],[0.150, 0.150, 0.150],[0.135, 0.075, 0.075],[0.115, 0.100, 0.075]]

        self.box_set3 = [[0.150, 0.150, 0.150],[0.100, 0.075, 0.075],[0.115, 0.100, 0.075],[0.195, 0.160, 0.150],[0.160, 0.125, 0.075],[0.195, 0.160, 0.075],
                         [0.150, 0.100, 0.075],[0.100, 0.100, 0.075],[0.115, 0.100, 0.075],[0.150, 0.150, 0.150],[0.160, 0.125, 0.075],[0.100, 0.100, 0.075],
                         [0.150, 0.100, 0.075],[0.100, 0.075, 0.075],[0.160, 0.125, 0.075],[0.100, 0.075, 0.075],[0.160, 0.075, 0.075],[0.100, 0.075, 0.075],[0.135, 0.075, 0.075],[0.150, 0.150, 0.150]]

        self.box_set4 = [[0.100, 0.075, 0.075],[0.195, 0.160, 0.150],[0.135, 0.075, 0.075],[0.195, 0.160, 0.150],[0.075, 0.075, 0.075],[0.075, 0.075, 0.075],
                         [0.150, 0.100, 0.075],[0.100, 0.100, 0.075],[0.135, 0.075, 0.075],[0.150, 0.100, 0.075],[0.150, 0.100, 0.075],[0.150, 0.150, 0.150],
                         [0.150, 0.150, 0.150],[0.075, 0.075, 0.075],[0.195, 0.160, 0.075],[0.100, 0.100, 0.075],[0.160, 0.125, 0.075],[0.160, 0.125, 0.075],[0.115, 0.100, 0.075],[0.150, 0.100, 0.075]]

        self.box_set5 = [[0.100, 0.100, 0.075],[0.160, 0.125, 0.075],[0.075, 0.075, 0.075],[0.100, 0.075, 0.075],[0.160, 0.125, 0.075],[0.075, 0.075, 0.075],
                         [0.160, 0.125, 0.075],[0.150, 0.150, 0.150],[0.150, 0.150, 0.150],[0.075, 0.075, 0.075],[0.160, 0.125, 0.075],[0.160, 0.125, 0.075],
                         [0.100, 0.075, 0.075],[0.115, 0.100, 0.075],[0.160, 0.125, 0.075],[0.100, 0.100, 0.075],[0.100, 0.075, 0.075],[0.195, 0.160, 0.075],[0.100, 0.100, 0.075],[0.075, 0.075, 0.075]]
                         
    def box_choice(self):
        if self.param_box.value == 1:
            box_set = self.box_set1
        elif self.param_box.value == 2:
            box_set = self.box_set2
        elif self.param_box.value == 3:
            box_set = self.box_set3            
        elif self.param_box.value == 4:
            box_set = self.box_set4 
        elif self.param_box.value == 5:
            box_set = self.box_set5
        return box_set                         
                         
    def get_box_sequently(self, box_set):
        box_set = np.array(box_set)
        box_set = np.asarray(box_set*1000, dtype = int)
        box_set = box_set.tolist()
        return box_set
    
    def put_box_sequently(self, box_set):
        box_set = self.box_sort(box_set)
        box_set = self.get_box_sequently(box_set)
        y_pos = self.calculate_y_pos(box_set)
        x_pos = self.calculate_x_pos(y_pos, box_set)
        x_pos = self.give_box_position(x_pos, y_pos)
        z_pos = self.calculate_z_pos(x_pos)
        x_pos, y_pos = self.give_pos(x_pos, y_pos, box_set)
        return x_pos, y_pos, z_pos, box_set
        
    def give_box_position(self, x_pos, y_pos):
        count = 0
        x_pos_list = []
        num = -1

        for i in range(len(y_pos)):
          if y_pos[i] == 0:
                num += 1
          x_pos_list.append(x_pos[num])
        
        return x_pos_list
    
    def calculate_y_pos(self, box_set):
        acum_y = 0
        count = 0
        y_pos=[]
        for i in range(20):
            if acum_y  +box_set[i][1] < 500:
                y_pos.append(acum_y)
            else :
                acum_y = 0
                y_pos.append(acum_y)
                
            acum_y += box_set[i][1]+5

        return y_pos

    
    def calculate_x_pos(self, y_pos, box_set):
        acum_x = 0
        num = 0
        count = 0
        x_pos=[] 
        x_list = [[0 for col in range(20)] for row in range(20)]
        layer_info = []
        for i in range(len(y_pos)):
            x_list[num][i] = box_set[i][0]
            if y_pos[i] == 0:
                if count == 0:
                    pass
                else:
                    layer_info.append(max(x_list[num]))
                count +=1
                num += 1
        print(layer_info)
        
        for i in range(len(layer_info)):
            if acum_x + layer_info[i] > 500:
                acum_x = 0
                x_pos.append(acum_x)
            else:
                x_pos.append(acum_x)
            acum_x +=layer_info[i]+5
            if i == len(layer_info)-1:
                if acum_x + box_set[i][0] < 500:
                    x_pos.append(acum_x)
                else :
                    x_pos.append(0)
        return x_pos

    def calculate_z_pos(self, x_pos):
        z_pos_info =[]
        z_pos = []
        count = 0
        num = 0
        for i in range(len(x_pos)):
            if x_pos[i] != 0:
                count = 1
            if count == 1:
              if x_pos[i] == 0:
                  num = 85
            z_pos.append(num)
        if x_pos[19] == 0:
            z_pos[19] = 225
        return z_pos

    def box_sort(self, box_set):
        box_set.sort(key=lambda x:x[0])
        box_set.sort(key=lambda x:x[2])
        return box_set
        
    def give_pos(self, x_pos, y_pos, box_set):
        for i in range(len(x_pos)):
            x_pos[i] += box_set[i][0]/2
            y_pos[i] += box_set[i][1]/2
        return x_pos, y_pos

class SpawnBoxOperator(Node): 
    def __init__(self):
        super().__init__('spawnbox_service_client')
        
        self.spawnbox_service_client = self.create_client(
            SpawnBox, 'spawnbox_operator')
            
    def send_request(self, box_info):
        request = SpawnBox.Request()
        request.spawn = True
        request.box_info = box_info
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
        
        self.gripper_client5 = self.create_client(
            SetBool, '/vacuum_gripper5/switch')
        self.gripper_client6 = self.create_client(
            SetBool, '/vacuum_gripper6/switch')                        
        self.gripper_client7 = self.create_client(
            SetBool, '/vacuum_gripper7/switch')           
        self.gripper_client8 = self.create_client(
            SetBool, '/vacuum_gripper8/switch')
           
         
    def send_gripper_on(self, num):
        request = SetBool.Request()
        request.data = True
        futures = self.gripper_client1.call_async(request)
        futures = self.gripper_client2.call_async(request)
        futures = self.gripper_client3.call_async(request)
        futures = self.gripper_client4.call_async(request)
        if num > 0:
        	futures = self.gripper_client5.call_async(request)
        	futures = self.gripper_client6.call_async(request)
        	futures = self.gripper_client7.call_async(request)
        	futures = self.gripper_client8.call_async(request)        

        return futures
        
    def send_gripper_off(self, num):
        request = SetBool.Request()
        request.data = False
        futures = self.gripper_client1.call_async(request)
        futures = self.gripper_client2.call_async(request)
        futures = self.gripper_client3.call_async(request)
        futures = self.gripper_client4.call_async(request)   
        if num > 0:
        	futures = self.gripper_client5.call_async(request)
        	futures = self.gripper_client6.call_async(request)
        	futures = self.gripper_client7.call_async(request)
        	futures = self.gripper_client8.call_async(request)    
        return futures     
        
            

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
    
    gripper = GripperOperator()
    
    algo = Algorithm()
    box_set = algo.box_choice()
    x_pos, y_pos, z_pos, box_set = algo.put_box_sequently(box_set)

    n = 0
    spawnbox = SpawnBoxOperator()
    future = spawnbox.send_request(box_set[n])
    #----------------------------------------------------------------
    robot = CDsrRobot()
    #----------------------------------------------------------------

    set_velx(100,100)  
    set_accx(100,100) 

    velx=[100, 100]
    accx=[100, 100]

    p2= posj(0.0, 0.0, 90.0, 0.0, 90.0, 0.0) #joint

    x1= posx(400, 500, 800.0, 0.0, 180.0, 0.0) #task
    x2= posx(400, 500, 500.0, 0.0, 180.0, 0.0) #task
    # 500
    pick_pos_up = posx(600, 0.0, 500.0, 0.0, 180.0, 0.0)

    num = 0
    while rclpy.ok(): 
        if box_set[n][2] == 150:
            num = 55
        else :
            num = 0
        pick_pos = posx(600, 0.0, num+100, 0.0, 180.0, 0.0)
        place_pos = posx(x_pos[n]+150, y_pos[n]-750, num+z_pos[n]+140.0, 0.0, 180.0, 0.0)
        place_pos_up = posx(x_pos[n]+150, y_pos[n]-750, 500.0, 0.0, 180.0, 0.0)
        
        # move joint    
        robot.movej(p2, vel=100, acc=100)
        print("------------> movej OK")    
        
        # move joint task : picking position  
        #robot.movel(pick_pos_up, velx, accx)
        #print("------------> movel OK")    
        
        # move line : move to pick    
        robot.movel(pick_pos, velx, accx)
        print("------------> movel OK")   
        future2 = gripper.send_gripper_on(num) 
        
        # picking - if get the true of /grasp picking topic
        # move line : move up
        robot.movel(pick_pos_up, velx, accx)
        print("------------> movel OK")    
     
        
        # move joint task : placing position  
        robot.movel(place_pos_up, velx, accx)
        print("------------> movel OK")    


        # move line : move to place
        robot.movel(place_pos, velx, accx)
        print("------------> movel OK")    

        # place
        gripper.send_gripper_off(num)
        n +=1
        # spawn box
        if n<20:
             spawnbox.send_request(box_set[n])
        else:
            pass       
        # move line : move up
        robot.movel(place_pos_up, velx, accx)
        print("------------> movel OK")    

        if n == 20:
            print("palletizing finished, Press (Ctrl + C) to close the window ")
            time.sleep(1000) 

    print('XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX good-bye!')
    print('XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX good-bye!')
    print('XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX good-bye!')

if __name__ == '__main__':
    main()
