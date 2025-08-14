#!/usr/bin/env python
import rospy
from geometry_msgs.msg import PoseStamped
from fast_lio.msg import RelocalizationMsg
from tf.transformations import quaternion_from_euler

rospy.init_node('localization_init_pose_pub')
pub = rospy.Publisher('/relocalization', RelocalizationMsg, queue_size=1, latch=True)

# Create RelocalizationMsg
relocalization_msg = RelocalizationMsg()

# Set PCD path
relocalization_msg.pcd_path = "/home/amov/PersonalData/Program/Ros/dispatch_ws/src/dispatch_control/Map/ntuitive/4/4.pcd"

# Set initial pose
relocalization_msg.init_pose = PoseStamped()
relocalization_msg.init_pose.header.frame_id = "map"
relocalization_msg.init_pose.header.stamp = rospy.Time.now()

relocalization_msg.init_pose.pose.position.x = -0.9900000095367432
relocalization_msg.init_pose.pose.position.y = 2.6600000858306885
relocalization_msg.init_pose.pose.position.z = 0

roll = 0.0
pitch = 0.0
yaw = 1.33

quaternion = quaternion_from_euler(roll, pitch, yaw)
relocalization_msg.init_pose.pose.orientation.x = quaternion[0]
relocalization_msg.init_pose.pose.orientation.y = quaternion[1]
relocalization_msg.init_pose.pose.orientation.z = quaternion[2]
relocalization_msg.init_pose.pose.orientation.w = quaternion[3]

pub.publish(relocalization_msg)
rospy.sleep(1.0)
