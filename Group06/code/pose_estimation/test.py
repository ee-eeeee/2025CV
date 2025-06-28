import cv2
import mediapipe as mp
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

if __name__ == '__main__':
    mp_pose = mp.solutions.pose
    pose = mp_pose.Pose(static_image_mode=True,
                        model_complexity=1,
                        smooth_landmarks=True,
                        min_detection_confidence=0.5,
                        min_tracking_confidence=0.5)
    drawing = mp.solutions.drawing_utils

    # 读取图像并转换为RGB
    img = cv2.imread("5.jpg")
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # 处理图像以获取关节点
    results = pose.process(img_rgb)

    # 绘制二维关节点
    if results.pose_landmarks:
        drawing.draw_landmarks(img, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

    # 显示二维图像
    cv2.imshow("keypoint", img)

    # 获取三维关节点坐标并绘制三维图像
    if results.pose_world_landmarks:
        # 获取三维关节点坐标
        landmarks = results.pose_world_landmarks.landmark

        # 创建三维图
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')

        # 绘制关节点
        for idx,landmark in enumerate(landmarks):
            x, y, z = landmark.x, landmark.y, landmark.z
            ax.scatter(x, z, -y)
            if idx == 11 or idx == 12 or idx == 15 or idx == 16 or idx == 23 or idx == 24:
                print(f"Landmark {idx}: (x={x}, y={y}, z={z})")

        # 绘制连接线
        connections = mp_pose.POSE_CONNECTIONS
        for connection in connections:
            start_idx = connection[0]
            end_idx = connection[1]
            start_landmark = landmarks[start_idx]
            end_landmark = landmarks[end_idx]
            ax.plot([start_landmark.x, end_landmark.x],
                    [start_landmark.z, end_landmark.z],
                    [-start_landmark.y, -end_landmark.y], 'b-')

        # 设置坐标轴范围
        ax.set_xlim([-1, 1])
        ax.set_ylim([-1, 1])
        ax.set_zlim([-1, 1])

        # 显示三维图像
        plt.show()

    # 等待用户按键并关闭窗口
    cv2.waitKey(0)
    cv2.destroyAllWindows()