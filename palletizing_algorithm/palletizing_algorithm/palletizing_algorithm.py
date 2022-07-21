import rclpy
import os
import sys
import threading, time
import signal

from rclpy.node import Node
from std_srvs.srv import *
from dsr_msgs2.msg import *
from dsr_msgs2.srv import *

class PalletizingAlgorithm(Node):
    def __init__(self):
        super().__init__('palletizing_algorithm')
        
        
class PositionInfo(Node):
    def __init__(self):
        super().__init__('position_information') 
        
        self.palletizing_pos_client = self.create_client(
            PalletPos, 'palletizing_pos')
        
    def send_pos_request(self):
         request = PalletPos.Request()
         request.x_pos = 0.3
         request.x_pos = 0.3
         request.x_pos = 0.3
         futures = self.palletizing_pos_client.call_async(request)
         return futures
        
        

def main():
    argv = sys.argv[1:]
    rclpy.init()
    palletizing = PalletizingAlgorithm()
    pos_info = PositionInfo() 

    node.get_logger().info("Done! Shutting down node.")
    rclpy.shutdown()           
        
if __name__ == "__main__":
    main()
