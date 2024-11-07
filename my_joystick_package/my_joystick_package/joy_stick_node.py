#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from pyjoystick.sdl2 import Key, Joystick, run_event_loop

class JoystickNode(Node):
    def __init__(self):
        super().__init__('joystick_node')
        
        #publisher
        self.publisher_ = self.create_publisher(Twist, 'cmd_vel', 10)

        # Initialize joystick
        self.speed = 1.0
        self.spin = 4.0
        self.left_stick_x = 0.0
        self.left_stick_y = 0.0
        self.right_stick_x = 0.0
        self.right_stick_y = 0.0
        
        # Start the joystick event loop using the provided structure
        run_event_loop(self.print_add, self.print_remove, self.key_received)

    def print_add(self, joy: Joystick):
        self.get_logger().info(f"Joystick connected: {joy}")

    def print_remove(self, joy: Joystick):
        self.get_logger().info(f"Joystick disconnected: {joy}")


    def key_received(self, key: Key):

        msg = Twist()
        msg.linear.x  = self.speed * self.left_stick_y
        msg.angular.z = self.spin * self.right_stick_x
        self.publisher_.publish(msg)

        pin  = key.number 
        type_input = key.keytype
        value = key.value
           # Handle axis movements
        if type_input == key.AXIS:
            match pin:
                case 0:
                    self.left_stick_x = -value
                case 1:
                    self.left_stick_y = -value
                case 3:
                    self.right_stick_x = -value
                case 4:
                    self.right_stick_y = -value
            return

        # PLAN TO MAKE 90 DEGREE BUTTON, Imma fix this one later        
        # if type_input == key.BUTTON:
        #     match pin:
        #         case 1:
        #             self.right_stick_x = -value
        #         case 3:
        #             self.left_stick_x = -value
        #     return

def main(args=None):
    rclpy.init(args=args)
    node = JoystickNode()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
