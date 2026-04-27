# LiDAR–IMU Sensor Fusion Motion Tracking (ROS 2)

## Overview

This project implements real-time motion tracking by combining MPU-6050 IMU data with RPLIDAR C1 scans on Raspberry Pi 5 using ROS 2 Jazzy Jalisco and rmw_zenoh.

Reference implementation:

---

## System Architecture

* **Sensors**

  * MPU6050 → `/imu/data`
  * RPLIDAR → `/scan`

* **Processing**

  * SLAM Toolbox → localization (TF)
  * EKF → IMU smoothing (optional)

* **Output**

  * TF tree (`map → odom → base_link`)
  * RViz visualization (map, scan, trajectory)

---

## Hardware Setup

### MPU6050 → Raspberry Pi 5 (I2C)

| MPU6050 | Raspberry Pi Pin |
| ------- | ---------------- |
| VCC     | 5V (Pin 2 or 4)  |
| GND     | GND              |
| SDA     | GPIO2 (Pin 3)    |
| SCL     | GPIO3 (Pin 5)    |

### RPLIDAR C1

* Connect via USB

---

## Raspberry Pi Setup (Ubuntu 24.04 Server)

Enable I2C:

```bash
sudo apt update
sudo apt install i2c-tools python3-smbus
sudo usermod -aG i2c $USER
sudo reboot
```

Verify MPU6050:

```bash
i2cdetect -y 1
```

Check LiDAR device:

```bash
ls /dev/ttyUSB*
```

Set permissions:

```bash
sudo chmod 666 /dev/ttyUSB0
```

---

## Software Requirements

* ROS 2 Jazzy
* slam_toolbox
* robot_localization
* rplidar_ros

Install:

```bash
sudo apt install ros-jazzy-slam-toolbox ros-jazzy-robot-localization
```

---

## Workspace Setup

```bash
mkdir -p ~/ros2_ws/src
cd ~/ros2_ws
colcon build
source install/setup.bash
```

Clone project:

```bash
cd ~/ros2_ws/src
git clone https://github.com/Aurevion/Handheld-motion-tracker.git
```

Build:

```bash
cd ~/ros2_ws
colcon build
source install/setup.bash
```

---

## Configuration

### EKF (`ekf.yaml`)

IMU-only configuration (no LiDAR odometry input).

### SLAM (`slam.yaml`)

Defines:

* `base_frame: base_link`
* `odom_frame: odom`
* `map_frame: map`
* `scan_topic: /scan`

---

## Run System

Start Zenoh (optional):

```bash
zenohd
```

Run system:

```bash
export RMW_IMPLEMENTATION=rmw_zenoh_cpp
source ~/ros2_ws/install/setup.bash
ros2 launch imu_mpu6050 system.launch.py
```

---

## Visualization (Laptop)

```bash
export RMW_IMPLEMENTATION=rmw_zenoh_cpp
rviz2
```

Add:

* TF
* LaserScan (`/scan`)
* Map

Set Fixed Frame:

```
map
```

---

## Expected Output

* LiDAR scan visible in RViz
* Map builds as sensor moves
* TF updates dynamically
* Robot trajectory appears

---

## Troubleshooting

### No movement / static output

```bash
ros2 topic echo /tf
```

### IMU not detected

```bash
i2cdetect -y 1
```

### LiDAR not working

```bash
ros2 topic echo /scan
```
