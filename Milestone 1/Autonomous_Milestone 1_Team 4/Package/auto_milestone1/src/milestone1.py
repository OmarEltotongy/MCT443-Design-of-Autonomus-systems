#!/usr/bin/env python3

import rospy  
from geometry_msgs.msg import Twist  
from auto_milestone1.srv import SetAngularVelocity, SetAngularVelocityResponse

# Initialize the current angular velocity to zero
current_angular_velocity = 0

def set_angular_velocity_callback(request):
    global current_angular_velocity

    # Get the requested angular velocity from the service request message
    requested_angular_velocity = request.angular_velocity

    # Set the current angular velocity to the requested value
    current_angular_velocity = requested_angular_velocity

    # Create a service response message with a "success" message
    response = SetAngularVelocityResponse()
    response.message = "Angular Velocity Set"

    return response

def main():
    global current_angular_velocity

    # Initialize a ROS node with the name 'husky_controller'
    rospy.init_node('husky_controller', anonymous=True)

    # Create a publisher that sends Twist messages to the '/husky_velocity_controller/cmd_vel' topic
    vel_pub = rospy.Publisher('/husky_velocity_controller/cmd_vel', Twist, queue_size=10)

    # Create a Twist message with a linear x velocity of 0.5 m/s and an angular z velocity of 0 rad/s
    vel_cmd = Twist()
    vel_cmd.linear.x = 0.5
    vel_cmd.angular.z = 0

    # Set the publishing rate to 10 Hz using a ROS Rate object
    rate = rospy.Rate(10)

    # Create a service that can be used to set the angular velocity of the robot
    set_angular_velocity_service = rospy.Service('/set_angular_velocity', SetAngularVelocity, set_angular_velocity_callback)

    try:
        while not rospy.is_shutdown():
            # Move the robot for 3 seconds
            for i in range(30):  # 10 Hz * 3 seconds = 30 iterations
                # Update the angular velocity of the Twist message with the current angular velocity
                vel_cmd.angular.z = current_angular_velocity

                # Publish the Twist message on the '/husky_velocity_controller/cmd_vel' topic
                vel_pub.publish(vel_cmd)

                # Sleep for the remaining time until 10 Hz is reached
                rate.sleep()

            # Stop the robot for 1 second
            vel_cmd.angular.z = 0
            vel_pub.publish(vel_cmd)
            rospy.sleep(1)

    except rospy.ROSInterruptException:
        pass

    # After the try-except block, set the angular velocity to 0 to stop the robot
    vel_cmd.angular.z = 0
    vel_pub.publish(vel_cmd)

if __name__ == '__main__':
    main()  # Call the main function
