from setuptools import find_packages, setup

package_name = 'orca_vision'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        (
            'share/ament_index/resource_index/packages',
            ['resource/' + package_name]
        ),
        (
            'share/' + package_name,
            ['package.xml']
        ),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='astroboy99',
    maintainer_email='astroboy99@example.com',
    description='Vision package for AUV ORCA',
    license='TODO',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'image_subscriber = orca_vision.image_subscriber:main',
            'subscriber_node = orca_vision.subscriber_node:main',
            'test_node = orca_vision.test_node:main',
            'qr_detector = orca_vision.qr_detector:main',
            'qr_validator = orca_vision.qr_validator:main',
        ],
    },
)
