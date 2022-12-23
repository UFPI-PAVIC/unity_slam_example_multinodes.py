import os
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.actions import OpaqueFunction
from launch.actions import DeclareLaunchArgument
from launch.launch_description_sources import PythonLaunchDescriptionSource
from ament_index_python.packages import get_package_share_directory
from launch_ros.actions import Node
from launch.substitutions import LaunchConfiguration
import os 


def launch_turtlebot3_nodes(context, *args, **kwargs):
    num_robots_var = LaunchConfiguration("num_robots").perform(context)
    
    turtle_list = list()
    
    for n in range(1, int(num_robots_var) + 1):
        turtle = Node(
                    package='turtlesim',
                    namespace='turtlesim_' + str(n),
                    executable='turtlesim_node',
                    name='turtle_' + str(n),
                    parameters=[{'use_sim_time':True}]
                    )
        
        turtle_list.append(turtle)
        
    return turtle_list

def generate_launch_description():
    package_name = 'unity_slam_example'
    package_dir = get_package_share_directory(package_name)
    DeclareLaunchArgument("num_robots", default_value='4')
    
    return LaunchDescription([
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                os.path.join(get_package_share_directory('ros_tcp_endpoint'), 'launch', 'endpoint.py')
            ),
        ),
        
        OpaqueFunction(function=launch_turtlebot3_nodes),
        
        Node(
            package='rviz2',
            executable='rviz2',
            output='screen',
            arguments=['-d', os.path.join(package_dir, 'nav2_unity.rviz'), '--ros-args', '--log-level', 'debug'],
            parameters=[{'use_sim_time':True}]
        ),

        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                os.path.join(get_package_share_directory('nav2_bringup'), 'launch', 'navigation_launch.py')
            ),
            launch_arguments={
                'use_sim_time': 'true'
            }.items()
        ),
        
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                os.path.join(get_package_share_directory('slam_toolbox'), 'launch', 'online_async_launch.py')
            ),
            launch_arguments={
                'use_sim_time': 'true'
            }.items()
        ),
    ])
