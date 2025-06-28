import cv2
import mediapipe as mp
import time

mp_pose = mp.solutions.pose
pose = mp_pose.Pose(static_image_mode=True,
                        model_complexity=1,
                        smooth_landmarks=True,
                        # enable_segmentation=True,
                        min_detection_confidence=0.5,
                        min_tracking_confidence=0.5)
mp_drawing = mp.solutions.drawing_utils

# 处理帧函数
def process_frame(img):
    # BGR转RGB
    img_RGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    # 将RGB图像输入模型，获取预测结果
    results = pose.process(img_RGB)

    # 可视化
    mp_drawing.draw_landmarks(img, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
    # look_img(img)
    # 在三维真实物理坐标系中可视化以米为单位的检测结果
    # mp_drawing.plot_landmarks(results.pose_world_landmarks, mp_pose.POSE_CONNECTIONS)

    # BGR转RGB
    # img_RGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    # 将RGB图像输入模型，获取预测结果
    # results = hands.process(img_RGB)

    # if results.multi_hand_landmarks: # 如果有检测到手
    #    # 遍历每一只检测出的手
    #    for hand_idx in range(len(results.multi_hand_landmarks)):
    #        hand_21 = results.multi_hand_landmarks[hand_idx] # 获取该手的所有关键点坐标
    #        mpDraw.draw_landmarks(img, hand_21, mp_hands.HAND_CONNECTIONS) # 可视化

    return img