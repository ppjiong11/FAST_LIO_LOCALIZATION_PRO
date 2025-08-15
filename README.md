# Multi-Floor Relocalization Based on fast_lio

## 📖 Introduction
本项目在 **fast_lio** 基础上实现了 **多楼层重定位** 功能，主要新增了 `scripts` 目录下的两个 Python 脚本：

1. **`init_pose_pub.py`**  
   - 使用 ROS 节点向 `/relocalization` 话题发布一个 `fast_lio/RelocalizationMsg` 消息  
   - 用于向 **fast_lio** 发送初始化位置和地图路径，从而触发重定位  

2. **`relocalization_handler.py`**  
   - 订阅 `/relocalization` 话题的 `fast_lio/RelocalizationMsg` 消息  
   - 收到消息后，依次执行：  
     1. **终止** 当前运行的 `fastlio_localization` 节点  
     2. **设置** 地图路径参数（`map_path`）  
     3. **重启** `fastlio_localization` 节点  
     4. **发布** 初始位姿到 `/init_pose` 话题（`geometry_msgs/PoseStamped`）  

---

## 🚀 Usage

1. **配置地图路径和初始位姿**  
   - 在 `init_pose_pub.py` 中修改：  
     - **地图路径** (`pcd_path`)  
     - **初始位姿** (x, y, z)  
     - **欧拉角** (roll, pitch, yaw)

2. **启动**  
   - 使用以下命令运行：
     ```bash
     roslaunch fast_lio localization_avia.launch
     ```
