#!/usr/bin/env python3

import rclpy
from rclpy.node import Node

from apriltag_msgs.msg import AprilTagDetectionArray


class AprilTagMonitor(Node):

    def __init__(self):
        super().__init__('apriltag_monitor')

        self.last_ids = None

        self.subscription = self.create_subscription(
            AprilTagDetectionArray,
            '/detections',
            self.detection_callback,
            10
        )

        self.get_logger().info('AprilTag Monitor started.')
        self.get_logger().info('Waiting for AprilTag detection...')

    def detection_callback(self, msg):

        detected_ids = sorted([
            detection.id
            for detection in msg.detections
        ])

        if detected_ids != self.last_ids:

            self.last_ids = detected_ids

            if detected_ids:
                self.get_logger().info(
                    f'Detected AprilTag ID(s): {detected_ids}'
                )

                for tag_id in detected_ids:
                    self.process_tag(tag_id)

            else:
                self.get_logger().info(
                    'No AprilTag detected.'
                )

    def process_tag(self, tag_id):

        mapping = {
            0: 'RYB',
            1: 'RBY',
            2: 'YRB',
            3: 'YBR',
            4: 'BRY',
            5: 'BYR'
        }

        sequence = mapping.get(tag_id)

        if sequence:
            self.get_logger().info(
                f'ID {tag_id} -> Color Sequence: {sequence}'
            )
        else:
            self.get_logger().warning(
                f'Unknown AprilTag ID: {tag_id}'
            )


def main(args=None):

    rclpy.init(args=args)

    node = AprilTagMonitor()

    try:
        rclpy.spin(node)

    except KeyboardInterrupt:
        pass

    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
