#!/usr/bin/env python
import rospy
from geometry_msgs.msg import PoseStamped
from tf.transformations import quaternion_from_euler

rospy.init_node('localization_init_pose_pub')
pub = rospy.Publisher('/init_pose', PoseStamped, queue_size=1, latch=True)

pose = PoseStamped()
pose.header.frame_id = "map"
pose.header.stamp = rospy.Time.now()

pose.pose.position.x = 2.6706125736236572
pose.pose.position.y = -0.891991138458252
pose.pose.position.z = -0.023643067106604576

pose.pose.orientation.x = 0.006836265325546265
pose.pose.orientation.y = -0.01048231497406959
pose.pose.orientation.z = -0.7697064280509949
pose.pose.orientation.w = 0.6382753252983093
# pose.pose.position.x = 2.4645559787750244
# pose.pose.position.y = -1.6284500360488892
# pose.pose.position.z = 1.41441810131073

# pose.pose.orientation.x = 0.2961534261703491
# pose.pose.orientation.y = 0.2344159185886383
# pose.pose.orientation.z = -0.6951290965080261
# pose.pose.orientation.w = 0.6116681098937988

pub.publish(pose)
rospy.sleep(1.0)
