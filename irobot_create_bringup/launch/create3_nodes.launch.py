#!/usr/bin/env python3
# Copyright 2021 iRobot Corporation. All Rights Reserved.
# @author Rodrigo Jose Causarano Nunez (rcausaran@irobot.com)
#
# Launch Create(R) 3 nodes

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import PathJoinSubstitution
from launch_ros.actions import Node


def generate_launch_description():
    # Directories
    pkg_create3_bringup = get_package_share_directory('irobot_create_bringup')
    pkg_create3_control = get_package_share_directory('irobot_create_control')

    # Paths
    control_launch_file = PathJoinSubstitution(
        [pkg_create3_control, 'launch', 'include', 'control.py'])
    hazards_params_yaml_file = PathJoinSubstitution(
        [pkg_create3_bringup, 'config', 'hazard_vector_params.yaml'])
    ir_intensity_params_yaml_file = PathJoinSubstitution(
        [pkg_create3_bringup, 'config', 'ir_intensity_vector_params.yaml'])
    wheel_status_params_yaml_file = PathJoinSubstitution(
        [pkg_create3_bringup, 'config', 'wheel_status_params.yaml'])
    mock_params_yaml_file = PathJoinSubstitution(
        [pkg_create3_bringup, 'config', 'mock_params.yaml'])

    # Includes
    diffdrive_controller = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([control_launch_file])
    )

    # Publish hazards vector
    hazards_vector_node = Node(
        package='irobot_create_toolbox',
        name='hazards_vector_node',
        executable='hazards_vector_publisher_node',
        parameters=[hazards_params_yaml_file,
                    {'use_sim_time': True}],
        output='screen',
    )

    # Publish IR intensity vector
    ir_intensity_vector_node = Node(
        package='irobot_create_toolbox',
        name='ir_intensity_vector_node',
        executable='ir_intensity_vector_publisher_node',
        parameters=[ir_intensity_params_yaml_file,
                    {'use_sim_time': True}],
        output='screen',
    )

    # Motion Control
    motion_control_node = Node(
        package='irobot_create_toolbox',
        name='motion_control',
        executable='motion_control',
        parameters=[{'use_sim_time': True}],
        output='screen',
    )

    # Publish wheel status
    wheel_status_node = Node(
        package='irobot_create_toolbox',
        name='wheel_status_publisher_node',
        executable='wheel_status_publisher_node',
        parameters=[wheel_status_params_yaml_file,
                    {'use_sim_time': True}],
        output='screen',
    )

    # Publish wheel status
    mock_topics_node = Node(
        package='irobot_create_toolbox',
        name='mock_publisher_node',
        executable='mock_publisher_node',
        parameters=[mock_params_yaml_file,
                    {'use_sim_time': True}],
        output='screen',
    )

    # Define LaunchDescription variable
    ld = LaunchDescription()
    # Include robot description
    ld.add_action(diffdrive_controller)
    # Add nodes to LaunchDescription
    ld.add_action(hazards_vector_node)
    ld.add_action(ir_intensity_vector_node)
    ld.add_action(motion_control_node)
    ld.add_action(wheel_status_node)
    ld.add_action(mock_topics_node)

    return ld