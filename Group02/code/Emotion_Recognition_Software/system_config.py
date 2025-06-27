import json
import os

class SystemConfig:
    def __init__(self):
        self.config_file = "system_config.json"
        self.default_config = {
            "emotion_colors": {
                "情绪1": "#1E90FF",  # 蓝色
                "情绪2": "#FFD700",  # 金黄色
                "情绪3": "#FF6347",  # 红色
                "情绪4": "#808080",  # 灰色
                "情绪5": "#00CED1",  # 青色
                "情绪6": "#90EE90",  # 浅绿色
                "情绪7": "#800080"   # 紫色
            },
            "max_frames": 600,
            "frame_rate": 30,
            "detection_interval": 20,  # 每20帧进行一次情绪识别
            "model_path": "emotion_recognition_model.h5"
        }
        
        self.config = self.load_config()
        
    def load_config(self):
        # 尝试加载配置文件
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                print(f"加载配置文件失败: {e}")
                
        # 如果加载失败，使用默认配置
        self.save_config(self.default_config)
        return self.default_config
        
    def save_config(self, config):
        # 保存配置文件
        with open(self.config_file, 'w') as f:
            json.dump(config, f, indent=4)
            
    def get_config(self, key):
        # 获取配置值
        return self.config.get(key, None)
        
    def set_config(self, key, value):
        # 设置配置值
        self.config[key] = value
        self.save_config(self.config)
        
    def get_emotion_color(self, emotion):
        # 获取情绪对应的显示颜色
        return self.config["emotion_colors"].get(emotion, "#000000")