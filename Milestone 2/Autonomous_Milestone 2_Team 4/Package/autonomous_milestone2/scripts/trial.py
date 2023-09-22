import rospy
import numpy as np
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from tf.transformations import euler_from_quaternion



def callback (Odometry):

    global theta_current

    
    
    orientation_q= Odometry.pose.pose.orientation
    orientation_q_list = [orientation_q.x , orientation_q.y , orientation_q.z , orientation_q.w]
    (roll, pitch, yaw) = euler_from_quaternion (orientation_q_list)
    if yaw > 0 :
    	theta_current = round (yaw, 3)
    else:
    	theta_current = round ((2*(np.pi) + yaw), 3)
    print ('theta' , round((theta_current*180)/np.pi,3))




   

rospy.init_node ('turtlebot3_control',anonymous=True)  
sub = rospy.Subscriber ('/odom',Odometry,callback)
rate = rospy.Rate (1)

while not rospy.is_shutdown():
 rate.sleep()	

