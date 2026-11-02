import cv2

import rclpy
from rclpy.node import Node

from sensor_msgs.msg import Image
from cv_bridge import CvBridge


class CameraViewer(Node):

    def __init__(self):
        super().__init__('camera_viewer')

        self.bridge = CvBridge()

        self.image_subscription = self.create_subscription(
            Image,
            '/image_raw',
            self.image_callback,
            10
        )

        self.get_logger().info(
            'Camera Viewer started'
        )

        self.get_logger().info(
            'Displaying /image_raw'
        )

    def image_callback(self, msg):

        try:
            frame = self.bridge.imgmsg_to_cv2(
                msg,
                desired_encoding='bgr8'
            )

        except Exception as error:
            self.get_logger().error(
                f'Failed to convert image: {error}'
            )
            return

        cv2.imshow(
            'ORCA Camera POV',
            frame
        )

        cv2.waitKey(1)


def main(args=None):

    rclpy.init(args=args)

    node = CameraViewer()

    try:
        rclpy.spin(node)

    except KeyboardInterrupt:
        pass

    finally:
        cv2.destroyAllWindows()

        node.destroy_node()

        rclpy.shutdown()


if __name__ == '__main__':
    main()
