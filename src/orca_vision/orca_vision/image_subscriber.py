import rclpy
from rclpy.node import Node

from sensor_msgs.msg import Image
from cv_bridge import CvBridge


class ImageSubscriber(Node):

    def __init__(self):
        super().__init__('image_subscriber')

        self.bridge = CvBridge()

        self.subscription = self.create_subscription(
            Image,
            '/camera/image_raw',
            self.image_callback,
            10
        )

    def image_callback(self, msg):
        try:
            frame = self.bridge.imgmsg_to_cv2(
                msg,
                desired_encoding='bgr8'
            )

            height, width, channels = frame.shape

            self.get_logger().info(
                f'Received image: {width}x{height} '
                f'channels={channels}'
            )

        except Exception as error:
            self.get_logger().error(
                f'Failed to convert image: {error}'
            )


def main(args=None):
    rclpy.init(args=args)

    node = ImageSubscriber()

    rclpy.spin(node)

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
