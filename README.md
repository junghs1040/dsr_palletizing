## 2022 대한통운 미래기술 경진대회      
#### Robot Palletizing Simulation Project      
Team : Seo & Jung Robotics (서앤정 로보틱스)       
      
### How to Start Palletizing      
#### 1. Start Gazebo and spawn the robot (Doosan robotics m1013)
<pre>
<code>
$ ros2 launch dsr_launcher2 single_robot_gazebo.launch.py
</code>
</pre>
      
#### 2. start palletizing with choosen set of boxes      
the following command is palletizing with box set 3      
<pre>
<code>
$ ros2 launch palletizing_control palletizing.launch.py 'box_set:=3'
</code>
</pre>
      
![Screenshot from 2022-07-28 14-46-30](https://user-images.githubusercontent.com/19335771/183271634-9929c94b-15c0-4ceb-b4a1-c9b3ce307676.png)
      
### Project Features

