
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
class Palletizing(Node):
    def __init__(self):
        super().__init__('palletizing') 
        self.pallet_width = 500
        self.pallet_length = 500
        self.pallet = np.zeros((self.pallet_width, self.pallet_length))
    
    def pallet_test(self, left_down_x,left_down_y, width, length):
        scope_test = self.scope_test(left_down_x,left_down_y, width, length)
        if scope_test !=0:
            print("Failed in pallet size test")
            return False

        #exist_test = self.exist_test(left_down_x,left_down_y, width, length)
        #if exist_test == False:
         #   return False
        return True
    
    # Test for Exceeding the Scope of the Pallet
    def scope_test(self, left_down_x,left_down_y, width, length):
        if left_down_x + width > self.pallet_width: 
            return 1
        if left_down_y + length > self.pallet_length: 
            return 2
        else :
            return 0
        
    def exist_test(self, left_down_x,left_down_y, width, length):
        for i in range(int(left_down_x), int(left_down_x)+width):
            for j in range(int(left_down_y), int(left_down_y)+length):
                if self.pallet[i][j] != 0:
                    print("Failed in box exist test")
                    return False
        print("Successed in pallet test")
        return True        
   
    def palletizing(self, ax, left_down_x, left_down_y, width, length):     
        test = self.pallet_test(left_down_x,left_down_y, width, length)
        if test == True:
            self.pallet_input(left_down_x,left_down_y, width, length)
            self.box_input(ax, left_down_x, left_down_y, width, length)
        else :
            print(False)
        

    
    def pallet_input(self, left_down_x,left_down_y, width, length):
        for i in range(int(left_down_x), int(left_down_x)+width):
            for j in range(int(left_down_y), int(left_down_y)+length):
                self.pallet[i][j] = 1     
                
    def box_input(self, ax, left_down_x, left_down_y, width, length):
        ax.add_patch(
           patches.Rectangle(
           (left_down_x, left_down_y),      # (x, y) coordinates of left-bottom corner point
           width, length,            # width, height
           edgecolor = 'black',
           fill = True,
           facecolor = 'red',
           ))
        
class Algorithm(Node):
    def __init__(self):
        super().__init__('palletizing_algorithm') 
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

                         
    def get_box_sequently(self, box_set):
        box_set = np.array(box_set)
        box_set = np.asarray(box_set*1000, dtype = int)
        box_set = box_set.tolist()
        return box_set
    
    def put_box_sequently(self, ax, palletizing, box_set):
        box_set = self.box_sort(box_set)
        box_set = self.get_box_sequently(box_set)
        y_pos = self.Algo1(box_set)
        print(y_pos)
        x_pos = self.Algo2(y_pos, box_set)
        x_pos = self.give_box_position(x_pos, y_pos)

        x_pos, y_pos = self.give_pos(x_pos, y_pos, box_set)
        
        return x_pos, y_pos, box_set
    def give_box_position(self, x_pos, y_pos):
        # z 값도 주는 함수 필요
        count = 0
        x_pos_list = []
        num = -1

        for i in range(len(y_pos)):
          if y_pos[i] == 0:
                num += 1
          x_pos_list.append(x_pos[num])
        
        return x_pos_list
    
    def Algo1(self, box_set):
        acum_y = 0
        count = 0
        y_pos=[]
        for i in range(20):
            if acum_y  + box_set[i][1] < 500:
                y_pos.append(acum_y)
            else :
                acum_y = 0
                y_pos.append(acum_y)
                
            acum_y += box_set[i][1]

        return y_pos

    
    def Algo2(self, y_pos, box_set):
        acum_x = 0
        num = 0
        count = 0
        x_pos=[] 
        layer_info = []
        for i in range(len(y_pos)):
            if y_pos[i] == 0:
                if count == 0:
                    pass
                else:
                    layer_info.append(box_set[i-1][0])
                count +=1
        print(layer_info)
        
        for i in range(len(layer_info)):
            if acum_x + layer_info[i] > 500:
                acum_x = 0
                x_pos.append(acum_x)
            else:
                x_pos.append(acum_x)
            acum_x +=layer_info[i]
            if i == len(layer_info)-1:
                x_pos.append(acum_x)
        return x_pos

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
    fig, ax = plt.subplots(figsize=(7, 7))
    ax.set_xlim(0.0, 500.0)
    ax.set_ylim(0.0, 500.0)
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    signal.signal(signal.SIGINT, signal_handler)
    
    gripper = GripperOperator()
    palletizing = Palletizing()
    #pallet_pos = GetPalletPos()
    
    algo = Algorithm()
    x_pos, y_pos, box_set = algo.put_box_sequently(ax, palletizing, algo.box_set1)
    
    n = 0
    spawnbox = SpawnBoxOperator()
    future = spawnbox.send_request(box_set[n])
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
    #place_pos = posx(400, -500, 150.0, 0.0, 180.0, 0.0)
    #place_pos_up = posx(400, -500, 500.0, 0.0, 180.0, 0.0)
    
    while rclpy.ok(): 
        
        place_pos = posx(x_pos[n]+150, y_pos[n]-750, 150.0, 0.0, 180.0, 0.0)
        place_pos_up = posx(x_pos[n]+150, y_pos[n]-750, 500.0, 0.0, 180.0, 0.0)
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
        n +=1
        # spawn box
        if n<20:
             spawnbox.send_request(box_set[n])
        else:
            pass       
        # move line : move up
        robot.movel(place_pos_up, velx, accx)
        print("------------> movel OK")    
        time.sleep(1)  
        if n == 20:
            print("palletizing finished")
            time.sleep(1000) 

    print('XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX good-bye!')
    print('XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX good-bye!')
    print('XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX good-bye!')

if __name__ == '__main__':
    main()
