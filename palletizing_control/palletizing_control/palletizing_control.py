import rclpy
import sys
import time 
import signal

import rclpy
import os, sys
import threading, time
import signal

from dsr_msgs2.msg import *

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

    #----------------------------------------------------------------
    robot = CDsrRobot()
    #----------------------------------------------------------------

    set_velx(30,20)  # set global task speed: 30(mm/sec), 20(deg/sec)
    set_accx(60,40)  # set global task accel: 60(mm/sec2), 40(deg/sec2)

    velx=[100, 100]
    accx=[100, 100]

    p2= posj(400, 500, 800.0, 0.0, 180.0, 0.0) #joint

    x1= posx(400, 500, 800.0, 0.0, 180.0, 0.0) #task
    x2= posx(400, 500, 500.0, 0.0, 180.0, 0.0) #task

    c1 = posx(559,434.5,651.5,0,180,0)
    c2 = posx(559,434.5,251.5,0,180,0)


    q0 = posj(0,0,0,0,0,0)
    q1 = posj(10, -10, 20, -30, 10, 20)
    q2 = posj(25, 0, 10, -50, 20, 40) 
    q3 = posj(50, 50, 50, 50, 50, 50) 
    q4 = posj(30, 10, 30, -20, 10, 60)
    q5 = posj(20, 20, 40, 20, 0, 90)
    qlist = [q0, q1, q2, q3, q4, q5]

    pick_pos = posx(400, 500, 80.0, 0.0, 180.0, 0.0)
    pick_pos_up = posx(400, 500, 800.0, 0.0, 180.0, 0.0)
    place_pos = posx(600, 750, 80, 0, 175, 0)
    place_pos_up = posx(600, 750, 600, 0, 175, 0)
    x3 = posx(150, 600, 450, 0, 175, 0)
    x4 = posx(-300, 300, 300, 0, 175, 0)
    x5 = posx(-200, 700, 500, 0, 175, 0)
    x6 = posx(600, 600, 400, 0, 175, 0)
    xlist = [x1, x2, x3, x4, x5, x6]


    X1 =  posx(370, 670, 650, 0, 180, 0)
    X1a = posx(370, 670, 400, 0, 180, 0)
    X1a2= posx(370, 545, 400, 0, 180, 0)
    X1b = posx(370, 595, 400, 0, 180, 0)
    X1b2= posx(370, 670, 400, 0, 180, 0)
    X1c = posx(370, 420, 150, 0, 180, 0)
    X1c2= posx(370, 545, 150, 0, 180, 0)
    X1d = posx(370, 670, 275, 0, 180, 0)
    X1d2= posx(370, 795, 150, 0, 180, 0)


    seg11 = posb(DR_LINE, X1, radius=20)
    seg12 = posb(DR_CIRCLE, X1a, X1a2, radius=21)
    seg14 = posb(DR_LINE, X1b2, radius=20)
    seg15 = posb(DR_CIRCLE, X1c, X1c2, radius=22)
    seg16 = posb(DR_CIRCLE, X1d, X1d2, radius=23)
    b_list1 = [seg11, seg12, seg14, seg15, seg16] 


    while rclpy.ok(): 
        # move joint    
        robot.movej(p2, vel=100, acc=100)
        print("------------> movej OK")    
        time.sleep(1)
        # move joint task : picking position  
        robot.movejx(pick_pos_up, vel=30, acc=60, sol=0)
        print("------------> movejx OK")    
        time.sleep(1)

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
        robot.movejx(place_pos_up, vel=30, acc=60, sol=0)
        print("------------> movejx OK")    
        time.sleep(1)

        # move line : move to pick    
        robot.movel(place_pos, velx, accx)
        print("------------> movel OK")    
        time.sleep(1)
        
        # picking - if get the true of /grasp picking topic
        # move line : move up
        robot.movel(place_pos_up, velx, accx)
        print("------------> movel OK")    
        time.sleep(1)   
 

    print('XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX good-bye!')
    print('XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX good-bye!')
    print('XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX good-bye!')

if __name__ == '__main__':
    main()
