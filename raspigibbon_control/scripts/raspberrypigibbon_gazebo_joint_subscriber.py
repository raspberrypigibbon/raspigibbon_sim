#!/usr/bin/env python 
# coding: utf-8 

import rospy
import math
from sensor_msgs.msg import JointState
from std_msgs.msg import Float64


class GazeboJoint:
    def __init__(self):
        self.sub = rospy.Subscriber('/raspigibbon/master_joint_state', JointState, self.joint_callback, queue_size=10)
        self.pub = {}
        for i in range(0,6):
            self.pub[i] = rospy.Publisher('/raspigibbon_on_gazebo/joint_' + str(i + 1) + '_position_controller/command', Float64, queue_size=10)
        self.r = rospy.Rate(10)

    def joint_callback(self, msg):
        if len(msg.position) > 0:
            for i in range(0,5):
                self.pub[i].publish(math.radians(msg.position[i]))
            self.pub[5].publish(math.radians(-msg.position[4]))
        self.r.sleep()

if __name__ == '__main__':
    try:
        while not rospy.is_shutdown():
            rospy.init_node('gazebo_joint_subscriber')
            dummy = GazeboJoint()
            rospy.spin()
    except rospy.ROSInterruptException:
        pass
