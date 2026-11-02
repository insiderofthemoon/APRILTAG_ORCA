import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class TestNode(Node):

    def __init__(self):
        super().__init__('test_node')

        self.publisher = self.create_publisher(
            String,
            '/vision_data',
            10
        )

        self.timer = self.create_timer(
            1.0,
            self.publish_data
        )

    def publish_data(self):
        msg = String()
        msg.data = 'ORCA Vision is alive!'
        self.publisher.publish(msg)

        self.get_logger().info(
            f'Publishing: {msg.data}'
        )


def main(args=None):
    rclpy.init(args=args)

    node = TestNode()

    rclpy.spin(node)

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
