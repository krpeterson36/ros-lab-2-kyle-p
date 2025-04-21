# Copyright 2016 Open Source Robotics Foundation, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import rclpy
import time
from rclpy.node import Node

from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan
            
class WallFollower(Node):
    def __init__(self):
        super().__init__('linear_publisher')
        self.publisher_ = self.create_publisher(Twist, '/peter494/diff_drive/cmd_vel', 1)
        self.subscription = self.create_subscription(LaserScan, '/peter494/diff_drive/scan', self.movement_callback, 10)
        self.desired_left_dist = 2.0
        self.kp = 0.5
        self.front_thresh = 3.0
        self.linear = 1.0        
    
    def movement_callback(self, msg):
        self.left_dist = msg.ranges[1]
        self.front_dist = msg.ranges[0]
        cmd = Twist()
        cmd.linear.x = self.linear

        if self.front_dist < self.front_thresh:
            cmd.angular.z = -self.kp
        elif self.left_dist > self.desired_left_dist:
            diff = self.left_dist - self.desired_left_dist
            cmd.angular.z = self.kp * diff
        else:
            cmd.angular.z = 0.0

        self.publisher_.publish(cmd)

def main(args=None):
    rclpy.init(args=args)

    wallFollower = WallFollower()

    rclpy.spin(wallFollower)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    wallFollower.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
