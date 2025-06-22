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

# 获取摄像头，传入0表示获取系统默认摄像头
cap = cv2.VideoCapture(0)

# 打开cap
cap.open(0)

# 无限循环，直到break被触发
while cap.isOpened():
    # 获取画面
    success, frame = cap.read()
    if not success:
        print('Error')
        break

    ## !!!处理帧函数
    frame = process_frame(frame)

    # 展示处理后的三通道图像
    cv2.imshow('my_window',frame)

    if cv2.waitKey(1) in [ord('q'),27]: # 按键盘上的q或esc退出（在英文输入法下）
        break

# 关闭摄像头
cap.release()
# 关闭图像窗口
cv2.destroyAllWindows()