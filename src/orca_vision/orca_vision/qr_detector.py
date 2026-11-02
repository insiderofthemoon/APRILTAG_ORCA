import rclpy
from rclpy.node import Node

from sensor_msgs.msg import Image
from std_msgs.msg import String

from cv_bridge import CvBridge
from pyzbar.pyzbar import decode


VALID_SEQUENCES = {
    'RYB',
    'RBY',
    'YRB',
    'YBR',
    'BRY',
    'BYR',
}


class QRDetector(Node):

    def __init__(self):
        super().__init__('qr_detector')

        self.bridge = CvBridge()

        # Subscribe to camera image
        self.image_subscription = self.create_subscription(
            Image,
            '/image_raw',
            self.image_callback,
            10
        )

        # Publish decoded QR result
        self.result_publisher = self.create_publisher(
            String,
            '/barcode/result',
            10
        )

        # Store the previous result to avoid publishing
        # the same QR continuously on every frame.
        self.last_result = None

        self.get_logger().info(
            'QR Detector started'
        )

        self.get_logger().info(
            'Listening to /image_raw'
        )

        self.get_logger().info(
            'Publishing results to /barcode/result'
        )

    def image_callback(self, msg):

        try:
            # Convert ROS Image message to OpenCV image
            frame = self.bridge.imgmsg_to_cv2(
                msg,
                desired_encoding='bgr8'
            )

        except Exception as error:
            self.get_logger().error(
                f'Failed to convert image: {error}'
            )
            return

        # Decode QR codes
        results = decode(frame)

        for result in results:

            # Only process QR codes
            if result.type != 'QRCODE':
                continue

            try:
                data = result.data.decode('utf-8')
            except UnicodeDecodeError:
                self.get_logger().warning(
                    'QR data could not be decoded as UTF-8'
                )
                continue

            # Check whether the QR contains one of our
            # six valid color sequences.
            if data not in VALID_SEQUENCES:
                self.get_logger().warning(
                    f'Unknown QR payload detected: {data}'
                )
                continue

            # Only publish when the result changes.
            if data != self.last_result:

                message = String()
                message.data = data

                self.result_publisher.publish(message)

                self.get_logger().info(
                    f'QR detected and published: {data}'
                )

                self.last_result = data


def main(args=None):

    rclpy.init(args=args)

    node = QRDetector()

    try:
        rclpy.spin(node)

    except KeyboardInterrupt:
        pass

    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
