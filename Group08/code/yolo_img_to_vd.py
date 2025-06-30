import os
import cv2
import glob
from tqdm import tqdm
from pathlib import Path
from ultralytics import YOLO

def yolo_predict_on_image_folder(image_folder, output_video_path, model_path='yolov8n.pt', conf_threshold=0.4):
    """
    使用YOLOv8原生API对指定文件夹中的所有图片进行目标检测，并将结果保存为视频
    
    参数:
        image_folder: 包含图片的文件夹路径
        output_video_path: 输出视频的保存路径
        model_path: YOLO模型路径，可以是预训练模型名称或本地模型路径
        conf_threshold: 置信度阈值，低于此值的检测框将被过滤
    """
    # 确保输出文件夹存在
    os.makedirs(os.path.dirname(output_video_path), exist_ok=True)
    
    # 加载YOLO模型
    print(f"正在加载{model_path}模型...")
    model = YOLO(model_path)
    
    # 获取图片文件列表
    image_extensions = ['*.jpg', '*.jpeg', '*.png', '*.bmp']
    image_files = []
    for ext in image_extensions:
        image_files.extend(glob.glob(os.path.join(image_folder, ext)))
    
    if not image_files:
        print(f"错误: 在{image_folder}中未找到图片文件")
        return
    
    # 按文件名排序
    image_files.sort()
    
    # 读取第一张图片以获取尺寸
    first_image = cv2.imread(image_files[0])
    height, width, _ = first_image.shape
    
    # 初始化视频写入器
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # 使用MP4格式
    fps = 2.0  # 视频帧率
    out = cv2.VideoWriter(output_video_path, fourcc, fps, (width, height))
    
    # 处理每张图片
    print(f"开始处理{len(image_files)}张图片...")
    for image_path in tqdm(image_files):
        # 读取图片
        img = cv2.imread(image_path)
        if img is None:
            print(f"警告: 无法读取图片 {image_path}，跳过")
            continue
        
        # 使用YOLOv8进行预测
        results = model(img, conf=conf_threshold, save=False)
        
        # 获取带检测框的图片
        result_img = results[0].plot()
        
        # 写入视频
        out.write(result_img)
    
    # 释放资源
    out.release()
    print(f"视频已保存至: {output_video_path}")

if __name__ == "__main__":
    # 设置参数
    IMAGE_FOLDER = "uav_dataset/train/20190925_134301_1_9"  # 替换为你的图片文件夹路径
    OUTPUT_VIDEO_PATH = "./detection_result1.mp4"  # 替换为你想要的输出视频路径
    MODEL_PATH = "train19/weights/best.pt"  # 可以是预训练模型名称或本地模型路径
    CONF_THRESHOLD = 0.4  # 置信度阈值
    
    # 运行预测
    yolo_predict_on_image_folder(
        image_folder=IMAGE_FOLDER,
        output_video_path=OUTPUT_VIDEO_PATH,
        model_path=MODEL_PATH,
        conf_threshold=CONF_THRESHOLD
    )