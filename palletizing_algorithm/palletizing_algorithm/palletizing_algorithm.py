import rclpy
import os
import sys
import threading, time
import signal

from rclpy.node import Node
from std_srvs.srv import *
from dsr_msgs2.msg import *
from dsr_msgs2.srv import *

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches


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
        print(box_set)
        y_pos = self.Algo1(box_set)
        print(y_pos)
        x_pos = self.Algo2(y_pos, box_set)
        x_pos = self.give_box_position(x_pos, y_pos)
        print(x_pos)

        for i in range(len(box_set)):
            palletizing.palletizing(ax, x_pos[i], y_pos[i], int(box_set[i][0]),int(box_set[i][1]))
        
        #palletizing.palletizing(ax, x_pos[2], y_pos[8], int(box_set[1][0]),int(box_set[1][1]))
        #palletizing.palletizing(ax, x_pos[2], y_pos[9], int(box_set[1][0]),int(box_set[1][1]))   
        
        
        return x_pos, y_pos
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

    # 층변경 알고리즘 필요
    def box_sort(self, box_set):
        box_set.sort(key=lambda x:x[0])
        box_set.sort(key=lambda x:x[2])
        return box_set

        
class PositionInfo(Node):
    def __init__(self):
        super().__init__('position_information') 
        
        self.palletizing_pos_client = self.create_client(
            PalletPos, 'palletizing_pos')
        
    def send_pos_request(self, x_pos, y_pos):
         request = PalletPos.Request()
         
         x_pos_ = []
         y_pos_ = []
         z_pos_ = [0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]
         for i in range(len(x_pos)):
              x_pos_.append(float(x_pos[i]))
              y_pos_.append(float(y_pos[i]))
         print(x_pos_)
         print(y_pos_)
         request.x_pos = x_pos_
         request.y_pos = y_pos_
         request.z_pos = z_pos_
         futures = self.palletizing_pos_client.call_async(request)      
         
         return futures.result()
        

def main():
    argv = sys.argv[1:]
    rclpy.init()
    fig, ax = plt.subplots(figsize=(7, 7))
    ax.set_xlim(0.0, 500.0)
    ax.set_ylim(0.0, 500.0)
    ax.set_xlabel('X')
    ax.set_ylabel('Y')

    palletizing = Palletizing()
    algo = Algorithm()
    
    x_pos, y_pos = algo.put_box_sequently(ax, palletizing, algo.box_set1)
    pos_info = PositionInfo() 
    response = pos_info.send_pos_request(x_pos, y_pos)
    print("send ok")
    
    #plt.show()
    #node.get_logger().info("Done! Shutting down node.")
    rclpy.shutdown()           
        
if __name__ == "__main__":
    main()
