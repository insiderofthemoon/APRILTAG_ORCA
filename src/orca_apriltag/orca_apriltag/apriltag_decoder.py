#!/usr/bin/env python3

import rclpy

from rclpy.node import Node
from std_msgs.msg import String
from apriltag_msgs.msg import AprilTagDetectionArray


class AprilTagDecoder(Node):

    def __init__(self):
        super().__init__('apriltag_decoder')

        # AprilTag ID to color sequence mapping
        self.tag_mapping = {
            0: 'RYB',
            1: 'RBY',
            2: 'YRB',
            3: 'YBR',
            4: 'BRY',
            5: 'BYR'
        }

        # Detection validation
        self.required_frames = 3
        self.reset_frames = 5

        self.candidate_id = None
        self.candidate_count = 0

        self.active_id = None
        self.empty_count = 0

        # Subscriber
        self.subscription = self.create_subscription(
            AprilTagDetectionArray,
            '/detections',
            self.detection_callback,
            10
        )

        # Publisher
        self.publisher = self.create_publisher(
            String,
            '/color_sequence',
            10
        )

        self.get_logger().info('AprilTag Decoder started.')
        self.get_logger().info('Waiting for AprilTag detections...')

    def detection_callback(self, msg):

        detected_ids = sorted(set(
            detection.id for detection in msg.detections
        ))

        # No marker detected
        if len(detected_ids) == 0:

            self.empty_count += 1

            self.candidate_id = None
            self.candidate_count = 0

            # Reset active marker after 5 empty frames
            if self.empty_count >= self.reset_frames:

                if self.active_id is not None:
                    self.get_logger().info(
                        'AprilTag removed. Ready for a new marker.'
                    )

                self.active_id = None

            return

        self.empty_count = 0

        # Multiple markers detected
        if len(detected_ids) > 1:

            self.candidate_id = None
            self.candidate_count = 0

            self.get_logger().warning(
                f'Multiple AprilTags detected: {detected_ids}. '
                'Show only one marker.'
            )

            return

        tag_id = detected_ids[0]

        # Validate ID
        if tag_id not in self.tag_mapping:

            self.candidate_id = None
            self.candidate_count = 0

            if self.active_id != tag_id:
                self.get_logger().warning(
                    f'Unknown AprilTag ID: {tag_id}'
                )
                self.active_id = tag_id

            return

        # Avoid publishing the same active marker repeatedly
        if tag_id == self.active_id:
            return

        # Temporal validation
        if tag_id == self.candidate_id:
            self.candidate_count += 1

        else:
            self.candidate_id = tag_id
            self.candidate_count = 1

        # Publish after stable detection
        if self.candidate_count >= self.required_frames:
            self.publish_sequence(tag_id)

    def publish_sequence(self, tag_id):

        sequence = self.tag_mapping[tag_id]

        msg = String()
        msg.data = sequence

        self.publisher.publish(msg)

        self.active_id = tag_id
        self.candidate_id = None
        self.candidate_count = 0

        self.get_logger().info(
            '===================================='
        )

        self.get_logger().info(
            f'AprilTag ID       : {tag_id}'
        )

        self.get_logger().info(
            f'Color Sequence    : {sequence}'
        )

        self.get_logger().info(
            'Published to      : /color_sequence'
        )

        self.get_logger().info(
            '===================================='
        )


def main(args=None):

    rclpy.init(args=args)

    node = AprilTagDecoder()

    try:
        rclpy.spin(node)

    except KeyboardInterrupt:
        pass

    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
