import rclpy
from rclpy.node import Node

from std_msgs.msg import String


MISSION_COMMANDS = {
    'RYB': 'COMMAND_1',
    'RBY': 'COMMAND_2',
    'YRB': 'COMMAND_3',
    'YBR': 'COMMAND_4',
    'BRY': 'COMMAND_5',
    'BYR': 'COMMAND_6',
}


MISSION_DESCRIPTIONS = {
    'RYB': 'Red -> Yellow -> Blue',
    'RBY': 'Red -> Blue -> Yellow',
    'YRB': 'Yellow -> Red -> Blue',
    'YBR': 'Yellow -> Blue -> Red',
    'BRY': 'Blue -> Red -> Yellow',
    'BYR': 'Blue -> Yellow -> Red',
}


class MissionDecisionNode(Node):

    def __init__(self):
        super().__init__('mission_decision_node')

        self.result_subscription = self.create_subscription(
            String,
            '/barcode/result',
            self.result_callback,
            10
        )

        self.last_sequence = None

        self.get_logger().info(
            'Mission Decision Node started'
        )

        self.get_logger().info(
            'Listening to /barcode/result'
        )

    def result_callback(self, msg):

        sequence = msg.data

        if sequence not in MISSION_COMMANDS:
            self.get_logger().warning(
                f'Unknown mission sequence received: {sequence}'
            )
            return

        command = MISSION_COMMANDS[sequence]
        description = MISSION_DESCRIPTIONS[sequence]

        # Ignore duplicate results
        if sequence == self.last_sequence:
            return

        self.last_sequence = sequence

        self.get_logger().info(
            '========================================'
        )

        self.get_logger().info(
            f'Received sequence: {sequence}'
        )

        self.get_logger().info(
            f'Mission: {description}'
        )

        self.get_logger().info(
            f'Mission command: {command}'
        )

        self.get_logger().info(
            f'Executing: {description}'
        )

        self.get_logger().info(
            '========================================'
        )


def main(args=None):

    rclpy.init(args=args)

    node = MissionDecisionNode()

    try:
        rclpy.spin(node)

    except KeyboardInterrupt:
        pass

    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
