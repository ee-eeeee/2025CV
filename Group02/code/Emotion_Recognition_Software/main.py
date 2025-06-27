import tkinter as tk
from tkinter import filedialog
import cv2
from video_processing import VideoProcessor
from emotion_visualization import EmotionVisualizer
from system_config import SystemConfig
import random  # 用于模拟情绪数据
from PIL import Image, ImageTk  # 用于图像转换
from data_processing import EmotionDataProcessor
import numpy as np
from RetinaFace.tools import FaceDetector
import torch

class MainInterface:
    def __init__(self, root):
        self.root = root
        self.root.title("长时间人脸情绪识别系统")
        self.root.geometry("1600x1200")

        self.config = SystemConfig()
        self.pic_num = 0
        self.pic_list = []
        self.video_processor = VideoProcessor()
        self.emotion_visualizer = EmotionVisualizer()
        self.emotion_data = EmotionDataProcessor(max_frames=self.config.get_config("max_frames"))

        self.is_camera_running = False
        self.is_processing_video = False

        face_det_model_path = "RetinaFace/Resnet50_Final.pth"
        self.face_detection = FaceDetector(face_det_model_path)

        self.setup_ui()

    def setup_ui(self):
        # 顶部标题
        title_label = tk.Label(self.root, text="长时间人脸情绪识别系统", font=("Arial", 18, "bold"))
        title_label.pack(pady=10)

        # 视频控制按钮区域
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=10)

        # 添加离线视频按钮
        self.offline_button = tk.Button(button_frame, text="离线视频", command=self.select_and_play_video,width=15,height=2,font=("Arial", 12, "bold"))
        self.offline_button.pack(side=tk.LEFT, padx=10)

        # 添加摄像头按钮
        self.camera_button = tk.Button(button_frame, text="实时摄像头", command=self.toggle_camera,width=15,height=2,font=("Arial",12,"bold"))
        self.camera_button.pack(side=tk.LEFT, padx=10)

        # 添加停止按钮
        self.stop_button = tk.Button(button_frame, text="停止", command=self.stop_all,width=15,height=2,font=("Arial",12,"bold"))
        self.stop_button.pack(side=tk.LEFT, padx=10)

        # 单一视频预览区域
        # 设置视频预览区域的宽度和高度，保持16:9的比例
        width = 60  # 你可以根据需要调整这个值
        height = int(width * 9 / 16)  # 计算高度以保持16:9的比例

        self.video_preview = tk.Label(self.root, text="视频预览区域", width=width, height=height, bg="black")
        self.video_preview.pack(fill=tk.BOTH, expand=True, padx=300, pady=10)

        # 创建一个底部容器，用于放置情绪条和情绪图例
        bottom_frame = tk.Frame(self.root)
        bottom_frame.pack(fill=tk.X, padx=20, pady=10, side=tk.BOTTOM)

        # 情绪条区域
        emotion_bar_frame = tk.LabelFrame(bottom_frame, text="情绪条", font=("Arial", 12))
        emotion_bar_frame.pack(fill=tk.X, padx=20, pady=10, side=tk.BOTTOM)  # 将情绪条放在底部容器的顶部

        # 使用EmotionVisualizer替代简单的Canvas
        self.emotion_visualizer.initialize_canvas(emotion_bar_frame, tk)

        # 情绪图例区域
        legend_frame = tk.Frame(bottom_frame)
        legend_frame.pack(fill=tk.X, padx=20, pady=10, side=tk.TOP)  # 将情绪图例放在底部容器的顶部

        # 创建情绪图例
        self.create_legend(legend_frame)

    def select_and_play_video(self):
        # 停止当前所有处理
        self.stop_all()
        self.pic_list = []

        # 选择新视频文件
        file_path = filedialog.askopenfilename(filetypes=[("视频文件", "*.mp4 *.avi *.mov")])
        if file_path:
            # 重置情绪数据
            self.emotion_data = EmotionDataProcessor(max_frames=self.config.get_config("max_frames"))

            # 加载并播放视频
            self.video_processor.load_video(file_path)
            self.is_processing_video = True
            self.process_video_frames()

    def toggle_camera(self):
        if self.is_camera_running:
            self.stop_camera()
        else:
            # 停止视频处理（如果有）
            self.is_processing_video = False
            # 重置情绪数据
            self.emotion_data = EmotionDataProcessor(max_frames=self.config.get_config("max_frames"))
            self.start_camera()

    def stop_all(self):
        """停止所有视频处理"""
        if self.is_processing_video:
            self.is_processing_video = False
        if self.is_camera_running:
            self.stop_camera()

        # 释放视频资源
        self.video_processor.release_all()
        self.pic_list = []

        # 清空预览区域
        self.video_preview.config(image=None)

    def start_camera(self):
        self.camera_button.config(text="关闭摄像头")
        self.pic_list = []
        self.is_camera_running = True
        self.video_processor.open_camera()
        self.process_camera_frames()

    def stop_camera(self):
        self.camera_button.config(text="实时摄像头")
        self.pic_list = []
        self.is_camera_running = False
        self.video_processor.close_camera()
        # 清空预览区域
        self.video_preview.config(image=None)

    def deal_pic(self, frame):
        face_left, face_top, face_right, face_bottom = self.face_detection.cal(frame)
        face = frame[face_top:face_bottom + 1, face_left:face_right + 1, :]
        face = cv2.resize(face, (48, 48))
        return face.astype(np.float32) / 255.0

    def process_video_frames(self):
        if not self.is_processing_video:
            return

        frame = self.video_processor.read_frame()
        if frame is None:
            self.is_processing_video = False
            return

        if self.pic_num % 15 == 0:
            self.pic_list.append(self.deal_pic(frame))
        self.pic_num += 1

        # 处理帧（人脸检测和情绪识别）
        if len(self.pic_list) == 3:
            emotion = self.video_processor.process_frame(self.pic_list)
            # 记录情绪数据并更新情绪条
            self.record_emotion_data(emotion)
            self.update_emotion_bar()
            self.pic_list = []
            self.pic_num = 0

        # 更新界面显示
        self.update_preview(frame)

        # 继续处理下一帧
        self.root.after(30, self.process_video_frames)

    def process_camera_frames(self):
        if not self.is_camera_running:
            return

        frame = self.video_processor.read_camera_frame()
        if frame is None:
            self.is_processing_video = False
            return

        if self.pic_num % 15 == 0:
            self.pic_list.append(self.deal_pic(frame))
        self.pic_num += 1

        # 处理帧（人脸检测和情绪识别）
        if len(self.pic_list) == 3:
            emotion = self.video_processor.process_frame(self.pic_list)
            # 记录情绪数据并更新情绪条
            self.record_emotion_data(emotion)
            self.update_emotion_bar()
            self.pic_list = []
            self.pic_num = 0

        # 更新界面显示
        self.update_preview(frame)

        # 继续处理下一帧
        self.root.after(30, self.process_camera_frames)

    def update_preview(self, frame):
        """更新视频预览区域"""
        # 将OpenCV BGR图像转换为RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # 获取预览区域的大小
        preview_width = self.video_preview.winfo_width()
        preview_height = self.video_preview.winfo_height()

        # 获取视频帧的大小
        height, width, _ = rgb_frame.shape

        # 计算宽高比
        aspect_ratio = width / height

        # 根据预览区域的大小和宽高比调整视频帧大小
        if preview_width / preview_height > aspect_ratio:
            # 预览区域更宽，以高度为标准
            new_height = preview_height
            new_width = int(new_height * aspect_ratio)
        else:
            # 预览区域更高，以宽度为标准
            new_width = preview_width
            new_height = int(new_width / aspect_ratio)

        # 调整图像大小
        rgb_frame = cv2.resize(rgb_frame, (new_width, new_height))

        # 转换为PIL图像，然后转换为ImageTk
        pil_image = Image.fromarray(rgb_frame)
        self.tk_image = ImageTk.PhotoImage(image=pil_image)

        # 更新标签
        self.video_preview.config(image=self.tk_image)
        self.video_preview.image = self.tk_image

    def record_emotion_data(self, emotion):
        emotions = ["others", "happiness", "sadness", "surprise", "disgust", "repression", "fear"]
        # 模拟随机情绪数据
        # print("emotion:", emotion)
        emotion = emotions[emotion]
        self.emotion_data.update_history(emotion)

    def update_emotion_bar(self):
        """更新情绪条显示"""
        emotion_trends = self.emotion_data.get_emotion_trends()
        self.emotion_visualizer.update_emotion_bar(emotion_trends)

    def create_legend(self, parent):
        """
        创建情绪图例

        参数:
            parent (tk.Widget): 父级容器
        """
        # 从配置中获取情绪颜色映射
        emotion_colors = self.config.get_config("emotion_colors")
        if not emotion_colors:
            # 如果配置中没有，使用默认的颜色映射
            emotion_colors = {
                "others": "#1E90FF",  # 蓝色
                "happiness": "#FFD700",  # 金黄色
                "sadness": "#FF6347",  # 红色
                "surprise": "#808080",  # 灰色
                "disgust": "#00CED1",  # 青色
                "repression": "#90EE90",  # 浅绿色
                "fear": "#800080"   # 紫色
            }

        # 创建图例项
        row = 0
        col = 0
        for emotion, color in emotion_colors.items():
            # 创建颜色块
            color_label = tk.Label(parent, text="■", fg=color, font=("Arial", 16))
            color_label.grid(row=row, column=col, padx=5, pady=2)

            # 创建情绪标签
            text_label = tk.Label(parent, text=emotion)
            text_label.grid(row=row, column=col+1, padx=5, pady=2)

            # 更新列位置
            col += 2


def fix_random_seeds():
    torch.manual_seed(42)
    np.random.seed(42)
    random.seed(42)
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False


if __name__ == "__main__":
    fix_random_seeds()
    root = tk.Tk()
    app = MainInterface(root)
    root.mainloop()
