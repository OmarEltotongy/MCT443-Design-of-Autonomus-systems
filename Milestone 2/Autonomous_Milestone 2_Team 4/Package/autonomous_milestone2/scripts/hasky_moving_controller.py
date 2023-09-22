import rospy
import numpy as np
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from tf.transformations import euler_from_quaternion

##Identifiy Global Variables##
#Polar coordinates 
global P
global alpha 
global beta
#Desired positions we require our robot to reach
global x_desired
global y_desired
global theta_desired
#Current positions our robot is at
global x_current
global y_current
global theta_current
#Control parameters
global linear_v	
global angular_v	
global Kp
global Kalpha
global Kbeta

## Parameter Initialize ##
linear_v  = 0
angular_v = 0
Kp = 0.5
Kalpha = 1.5
Kbeta = -0.5
x_current = 0
y_current = 0
theta_current = 0

def callback (Odometry):
    global x_current
    global y_current
    global theta_current

    x_current = round (Odometry.pose.pose.position.x,3)
    print ("sub_ x:  ", x_current)
    y_current = round (Odometry.pose.pose.position.y,3)
    print ("sub_ y:  ", y_current)
    
    orientation_q= Odometry.pose.pose.orientation
    orientation_q_list = [orientation_q.x , orientation_q.y , orientation_q.z , orientation_q.w]
    (roll, pitch, yaw) = euler_from_quaternion (orientation_q_list)
    theta_current = round (yaw, 3)
    print ('theta' , (theta_current*180)/np.pi)



def Polar_Coordinates():
    global x_desired
    global y_desired
    global theta_desired
    global P
    global alpha
    global beta
    global x_current
    global y_current
    global theta_current

    delta_x = x_desired - x_current
    delta_y = y_desired - y_current

    P = np.sqrt((np.square (delta_x))+(np.square (delta_y)))
    print ("P: " , P)
    tot_angle = np.arctan2 (delta_y,delta_x)

    if tot_angle < 0:
        tot_angle = tot_angle + (np.pi *2)
    
    alpha = tot_angle - theta_current
    print ('a: ' , alpha)
    beta = - alpha - theta_current + ((theta_desired*np.pi)/180)
    print ('b: ', beta)


def Control_Law():
    global P		
    global beta		 
    global alpha		
    global linear_v	
    global angular_v	
    global Kp
    global Kalpha
    global Kbeta 

    if np.absolute (alpha) < (np.pi)/2:
        linear_v = Kp * P
    else:
        linear_v = -Kp * P
    angular_v = Kalpha * alpha + Kbeta * beta 


if __name__ == '__main__':
#    global x_desired
#    global y_desired
#    global theta_desired
#    global P
#    global alpha
#    global beta

    x_desired = float (input ("Desired X goal: "))
    y_desired = float (input ("Desired Y goal: "))
    theta_desired = float (input ("Desired Theta goal in deg: "))

    rospy.init_node ('turtlebot3_control',anonymous=True)
    pub = rospy.Publisher ('/cmd_vel',Twist,queue_size=10)
    rate = rospy.Rate (10)
    sub = rospy.Subscriber ('/odometry/filtered',Odometry,callback)
    vel_msg = Twist()

    while not rospy.is_shutdown():

        Polar_Coordinates()
        Control_Law()

        v = round(linear_v,2)
        print ('v: ', v)
        w = round(angular_v,2)
        print('w: ',w)

        #Set the values of the Twist msg to be published
        vel_msg.linear.x = v  #Linear Velocity
        vel_msg.linear.y = 0
        vel_msg.linear.z = 0
        vel_msg.angular.x = 0
        vel_msg.angular.y = 0
        vel_msg.angular.z = w #Angular Velocity

    	#ROS Code Publisher
        pub.publish(vel_msg)	#Publish msg
        rate.sleep()			#Sleep with rate

