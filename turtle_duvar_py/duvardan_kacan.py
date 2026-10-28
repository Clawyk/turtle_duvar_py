#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
try:
    from turtlesim.msg import Pose
except ModuleNotFoundError:
    from turtlesim_msgs.msg import Pose

class DuvardanKacanTurtle(Node):
    def __init__(self):
        super().__init__('duvardan_kacan_node')

        self.declare_parameter('dogrusal_hiz', 2.0)
        self.declare_parameter('acisal_hiz', 1.5)
        self.declare_parameter('alt_sinir', 1.0)
        self.declare_parameter('ust_sinir', 10.0)

        self.publisher_ = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)

        self.subscription = self.create_subscription(
            Pose,
            '/turtle1/pose',
            self.pose_callback,
            10
        )

        self.log_timer = self.create_timer(1.0, self.log_konum)
        
        self.guncel_pose = None
        self.get_logger().info("Duvardan kaçan kaplumbağa düğümü başlatıldı!")

    def pose_callback(self, msg):
        self.guncel_pose = msg

        v_lin = self.get_parameter('dogrusal_hiz').get_parameter_value().double_value
        v_ang = self.get_parameter('acisal_hiz').get_parameter_value().double_value
        min_b = self.get_parameter('alt_sinir').get_parameter_value().double_value
        max_b = self.get_parameter('ust_sinir').get_parameter_value().double_value

        hareket = Twist()

        if msg.x < min_b or msg.x > max_b or msg.y < min_b or msg.y > max_b:
            hareket.linear.x = v_lin * 0.5  # Çarpmamak için biraz yavaşla
            hareket.angular.z = v_ang       # Dönüş yap
        else:
            hareket.linear.x = v_lin
            hareket.angular.z = 0.0

        self.publisher_.publish(hareket)

    def log_konum(self):
        if self.guncel_pose is not None:
            self.get_logger().info(f"Konum -> X: {self.guncel_pose.x:.2f}, Y: {self.guncel_pose.y:.2f}")

def main(args=None):
    rclpy.init(args=args)
    node = DuvardanKacanTurtle()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
