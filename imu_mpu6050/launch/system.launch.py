from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import ExecuteProcess, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from ament_index_python.packages import get_package_share_directory
import os

def generate_launch_description():

    pkg_share = get_package_share_directory('imu_mpu6050')
    ekf_config = os.path.join(pkg_share, 'config', 'ekf.yaml')
    slam_config = os.path.join(pkg_share, 'config', 'slam.yaml')

    return LaunchDescription([

        # IMU node
        Node(
            package='imu_mpu6050',
            executable='imu_node',
            name='imu_node',
            output='screen'
        ),

        # RPLIDAR
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                os.path.join(
                    get_package_share_directory('rplidar_ros'),
                    'launch',
                    'rplidar_c1_launch.py'
                )
            )
        ),

        # SLAM Toolbox with config
        Node(
            package='slam_toolbox',
            executable='async_slam_toolbox_node',
            name='slam_toolbox',
            output='screen',
            parameters=[slam_config]  # FIXED: Load configuration
        ),

        # EKF fusion
        Node(
            package='robot_localization',
            executable='ekf_node',
            name='ekf_filter_node',
            output='screen',
            parameters=[ekf_config]
        ),

        # Static TF: base_link -> imu
        Node(
            package='tf2_ros',
            executable='static_transform_publisher',
            arguments=['0','0','0','0','0','0','base_link','imu_link']
        ),

        # Static TF: base_link -> lidar
        Node(
            package='tf2_ros',
            executable='static_transform_publisher',
            arguments=['0','0','0','0','0','0','base_link','laser']
        ),
    ])
