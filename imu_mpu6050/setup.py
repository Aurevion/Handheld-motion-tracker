from setuptools import find_packages, setup

package_name = 'imu_mpu6050'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),  # FIXED
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/imu_mpu6050/launch', ['launch/system.launch.py']),
        ('share/imu_mpu6050/config', ['config/ekf.yaml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='solomon',
    maintainer_email='raghavrawat04@gmail.com',
    description='IMU MPU6050 ROS2 driver',
    license='Apache-2.0',
    entry_points={
        'console_scripts': [
            'imu_node = imu_mpu6050.imu_node:main',
        ],
    },
)