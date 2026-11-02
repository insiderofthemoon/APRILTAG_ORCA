from collections import Counter, deque

import rclpy
from rclpy.node import Node

from std_msgs.msg import String


VALID_SEQUENCES = {
    'RYB',
    'RBY',
    'YRB',
    'YBR',
    'BRY',
    'BYR',
}

WINDOW_SIZE = 10
MIN_CONFIDENCE = 0.70


class QRValidator(Node):

    def __init__(self):
        super().__init__('qr_validator')

        self.history = deque(maxlen=WINDOW_SIZE)

        self.detection_subscription = self.create_subscription(
            String,
            '/barcode/detection',
            self.detection_callback,
            10
        )

        self.result_publisher = self.create_publisher(
            String,
            '/barcode/result',
            10
        )

        self.last_published_result = None

        self.get_logger().info(
            'QR Validator started'
        )

        self.get_logger().info(
            f'Window size: {WINDOW_SIZE}'
        )

        self.get_logger().info(
            f'Minimum confidence: {MIN_CONFIDENCE:.2f}'
        )

    def detection_callback(self, msg):

        sequence = msg.data

        if sequence not in VALID_SEQUENCES:
            return

        self.history.append(sequence)

        # Wait until the voting window is full
        if len(self.history) < WINDOW_SIZE:
            self.get_logger().info(
                f'Collecting detections: '
                f'{len(self.history)}/{WINDOW_SIZE}'
            )
            return

        counts = Counter(self.history)

        winning_sequence, winning_count = counts.most_common(1)[0]

        confidence = winning_count / WINDOW_SIZE

        self.get_logger().info(
            f'Voting result: {winning_sequence} '
            f'({winning_count}/{WINDOW_SIZE}) '
            f'confidence={confidence:.2f}'
        )

        if confidence < MIN_CONFIDENCE:
            self.get_logger().warning(
                'QR result rejected: confidence too low'
            )
            return

        # Avoid repeatedly publishing the same validated result
        if winning_sequence == self.last_published_result:
            return

        result_message = String()

        result_message.data = winning_sequence

        self.result_publisher.publish(result_message)

        self.last_published_result = winning_sequence

        self.get_logger().info(
            f'VALID QR RESULT: {winning_sequence} '
            f'confidence={confidence:.2f}'
        )


def main(args=None):

    rclpy.init(args=args)

    node = QRValidator()

    try:
        rclpy.spin(node)

    except KeyboardInterrupt:
        pass

    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
