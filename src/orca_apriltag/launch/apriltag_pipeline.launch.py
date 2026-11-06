from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
import os


def generate_launch_description():

    # Camera configuration
    camera_device = LaunchConfiguration('camera_device')

    # AprilTag configuration file
    config_file = os.path.expanduser(
        '~/orca_ws/apriltag_project/config/apriltag.yaml'
    )

    # USB Camera Node
    camera_node = Node(
        package='v4l2_camera',
        executable='v4l2_camera_node',
        name='camera',
        output='screen',
        parameters=[{
            'video_device': camera_device,
            'image_size': [640, 480],
            'pixel_format': 'YUYV',
        }]
    )

    # AprilTag Detector Node
    apriltag_node = Node(
        package='apriltag_ros',
        executable='apriltag_node',
        name='apriltag',
        output='screen',
        remappings=[
            ('image_rect', '/image_raw'),
            ('camera_info', '/camera_info'),
        ],
        parameters=[config_file]
    )

    return LaunchDescription([
        DeclareLaunchArgument(
            'camera_device',
            default_value='/dev/video2',
            description='USB camera device'
        ),

        camera_node,
        apriltag_node,
    ])
