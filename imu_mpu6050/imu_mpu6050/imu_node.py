import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Imu
import smbus
import math
import time

MPU_ADDR = 0x68

class IMUNode(Node):
    def __init__(self):
        super().__init__('imu_node')
        self.pub = self.create_publisher(Imu, '/imu/data', 10)
        self.timer = self.create_timer(0.01, self.read_imu)
        self.bus = smbus.SMBus(1)

        # Wake MPU6050
        self.bus.write_byte_data(MPU_ADDR, 0x6B, 0)

    def read_word(self, reg):
        high = self.bus.read_byte_data(MPU_ADDR, reg)
        low = self.bus.read_byte_data(MPU_ADDR, reg+1)
        val = (high << 8) + low
        if val >= 0x8000:
            val = -((65535 - val) + 1)
        return val

    def read_imu(self):
        msg = Imu()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.header.frame_id = "imu_link"

        ax = self.read_word(0x3B) / 16384.0
        ay = self.read_word(0x3D) / 16384.0
        az = self.read_word(0x3F) / 16384.0

        gx = self.read_word(0x43) / 131.0
        gy = self.read_word(0x45) / 131.0
        gz = self.read_word(0x47) / 131.0

        msg.linear_acceleration.x = ax * 9.81
        msg.linear_acceleration.y = ay * 9.81
        msg.linear_acceleration.z = az * 9.81

        msg.angular_velocity.x = math.radians(gx)
        msg.angular_velocity.y = math.radians(gy)
        msg.angular_velocity.z = math.radians(gz)

        self.pub.publish(msg)

def main():
    rclpy.init()
    node = IMUNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()