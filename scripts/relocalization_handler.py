#!/usr/bin/env python

import rospy
import subprocess
import time
import signal
import os
from fast_lio.msg import RelocalizationMsg
from geometry_msgs.msg import PoseStamped

class RelocalizationHandler:
    def __init__(self):
        rospy.init_node('relocalization_handler')
        self.fastlio_process = None
        self.init_pose_pub = rospy.Publisher('/init_pose', PoseStamped, queue_size=1, latch=True)
        
        # Subscribe to relocalization messages
        self.relocalization_sub = rospy.Subscriber('/relocalization', RelocalizationMsg, self.handle_relocalization)
        
        rospy.loginfo("Relocalization handler started. Waiting for relocalization messages...")

    def kill_fastlio_node(self):
        """Kill the fastlio_localization node if it exists"""
        try:
            # Find and kill the fastlio_localization process
            result = subprocess.run(['pkill', '-f', 'fastlio_localization'], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                rospy.loginfo("Successfully killed fastlio_localization node")
                time.sleep(1)  # Wait for process to fully terminate
            else:
                rospy.logwarn("No fastlio_localization process found to kill")
        except Exception as e:
            rospy.logerr(f"Error killing fastlio_localization node: {e}")

    def set_map_path_param(self, pcd_path):
        """Set the map_path parameter"""
        try:
            rospy.set_param('/map_path', pcd_path)
            rospy.loginfo(f"Set map_path parameter to: {pcd_path}")
        except Exception as e:
            rospy.logerr(f"Error setting map_path parameter: {e}")

    def restart_fastlio_node(self):
        """Restart the fastlio_localization node"""
        try:
            # Command to launch the fastlio_localization node
            cmd = ['rosrun', 'fast_lio', 'fastlio_localization']
            
            # Start the process
            self.fastlio_process = subprocess.Popen(cmd, 
                                                   stdout=subprocess.PIPE, 
                                                   stderr=subprocess.PIPE)
            rospy.loginfo("Successfully restarted fastlio_localization node")
            
        except Exception as e:
            rospy.logerr(f"Error restarting fastlio_localization node: {e}")

    def publish_init_pose(self, init_pose):
        """Publish the initial pose after 1 second delay"""
        try:            
            # Directly publish the PoseStamped message
            pose_msg = PoseStamped()
            pose_msg.header = init_pose.header
            pose_msg.pose = init_pose.pose
            
            self.init_pose_pub.publish(pose_msg)
            rospy.loginfo("Published initial pose to /init_pose")
            
        except Exception as e:
            rospy.logerr(f"Error publishing initial pose: {e}")

    def handle_relocalization(self, msg):
        """Handle incoming relocalization messages"""
        rospy.loginfo("Received relocalization message")
        rospy.loginfo(f"PCD Path: {msg.pcd_path}")
        
        # Step 1: Kill existing fastlio_localization node
        self.kill_fastlio_node()
        
        # Step 2: Set the map_path parameter
        self.set_map_path_param(msg.pcd_path)
        
        # Step 3: Restart fastlio_localization node
        self.restart_fastlio_node()
        
        # Step 4: Publish init_pose)
        self.publish_init_pose(msg.init_pose)

    def cleanup(self):
        """Cleanup function to kill the process on shutdown"""
        if self.fastlio_process and self.fastlio_process.poll() is None:
            self.fastlio_process.terminate()
            self.fastlio_process.wait()

if __name__ == '__main__':
    try:
        handler = RelocalizationHandler()
        rospy.on_shutdown(handler.cleanup)
        rospy.spin()
    except rospy.ROSInterruptException:
        pass