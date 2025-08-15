# Introduction
本项目是基于fastlio的多楼层重定位代码。
主要添加了scrpts中的两个py文件。
首先 init_pose_pub.py是利用ros节点向/relocalization 话题发布一个 fast_lio/RelocalizationMsg 消息，用来让 fast_lio 进行重定位（初始化位置和地图路径）。
relocalization_handler.py 首先订阅fast_lio/RelocalizationMsg，收到后kill掉当前运行的 fastlio_localization 节点 → 设置地图路径参数（map_path） → 重启 fastlio_localization 节点 → 向 /init_pose 话题发布初始位姿（geometry_msgs/PoseStamped）。

# usage
地图路径和初始位姿以及欧拉角在init_pose_pub.py里；
直接用localization_avia.launch文件启动。
