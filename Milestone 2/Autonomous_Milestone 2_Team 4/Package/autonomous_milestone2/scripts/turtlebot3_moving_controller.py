import rospy
import numpy as np                    #import numpy for trignometric function, arrays... etc
from geometry_msgs.msg import Twist   #import msg data type "Twist" to be published
from nav_msgs.msg import Odometry     #import msg data type "Odometry" to be subscribed
from tf.transformations import euler_from_quaternion  #import a Function for the Conversion from Quaternion transformation to Euler transformation

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
Kp = 0.3
Kalpha = 1
Kbeta = -0.5
x_current = 0
y_current = 0
theta_current = 0

def callback (Odometry):   #Callback function with the information we subscribed to which is /odom
    global x_current
    global y_current
    global theta_current

    x_current = round (Odometry.pose.pose.position.x,3)  #Get the robot's position in X
    print ("sub_ x:  ", x_current)
    y_current = round (Odometry.pose.pose.position.y,3)  #Get the robot's position in Y
    print ("sub_ y:  ", y_current)
    
    #Conversion from Quaternion transformation to Euler transformation
    orientation_q= Odometry.pose.pose.orientation
    orientation_q_list = [orientation_q.x , orientation_q.y , orientation_q.z , orientation_q.w]
    (roll, pitch, yaw) = euler_from_quaternion (orientation_q_list)
    
    #Condition to avoid negative angles after 180 deg in turtlebot3, where theta_current will vary bet. 0 to 360
    if yaw > 0 :
        theta_current = round (yaw, 3)
    else:
        theta_current = round ((2*(np.pi) + yaw), 3)
    print ('theta' , round((theta_current*180)/np.pi,3))


def Polar_Coordinates():    #Calculate polar coordinates
    global x_desired
    global y_desired
    global theta_desired
    global P
    global alpha
    global beta
    global x_current
    global y_current
    global theta_current

    delta_x = x_desired - x_current     #Calculate the Difference in X direction
    delta_y = y_desired - y_current     #Calculate the Difference in Y direction

    #Calculate the distance between the desired and the current position
    P = np.sqrt((np.square (delta_x))+(np.square (delta_y)))
    print ("P: " , P)

    tot_angle = np.arctan2 (delta_y,delta_x)   #Calculate angle between the global X-direction of the Mobile Robot and p

    if tot_angle < 0:
        tot_angle = tot_angle + (np.pi *2)
    
    alpha = tot_angle - theta_current        #Calculate angle between the local X-direction of the Mobile Robot and p
    print ('a: ' , (alpha*180)/np.pi)

    beta = - alpha - theta_current + ((theta_desired*np.pi)/180)   #Calculate angle between p and desired global X-direction of the Mobile Robot
    print ('b: ', (beta*180)/np.pi)


def Control_Law():   #Control function to move the Mobile Robot
    global P		
    global beta		 
    global alpha		
    global linear_v	
    global angular_v	
    global Kp
    global Kalpha
    global Kbeta 

     #Calculate controlled linear velocity and angular velocity

    if np.absolute (alpha) < (np.pi)/2:    #IF condition is incase the point is behind the robot
        linear_v = Kp * P
    else:
        linear_v = -Kp * P                 #This allows the Mobile robot to move backwards with a negative velocity

    angular_v = Kalpha * alpha + Kbeta * beta 


if __name__ == '__main__':
#    global x_desired
#    global y_desired
#    global theta_desired
#    global P
#    global alpha
#    global beta

    #Input your desired coordinates
    x_desired = float (input ("Desired X goal: "))
    y_desired = float (input ("Desired Y goal: "))
    theta_desired = float (input ("Desired Theta goal in deg: "))

    #Node, Publisher and Subscriber Setup
    rospy.init_node ('turtlebot3_control',anonymous=True)          #Initialize ROS node
    pub = rospy.Publisher ('/cmd_vel',Twist,queue_size=10)         #Publish to velocity commands to the turtlebot3 topic 
    rate = rospy.Rate (10)                                         # rate of publishing msg 10hz
    sub = rospy.Subscriber ('/odom',Odometry,callback)             #Subscribe to the Odometry topic to get feedback on the position
    vel_msg = Twist()

    while not rospy.is_shutdown():

        Polar_Coordinates()
        Control_Law()

        #Calculate the linear and angular velocities
        v = round(linear_v,2)    #Linear Velocity
        print ('v: ', v)
        w = round(angular_v,2)   #Angular Velocity
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