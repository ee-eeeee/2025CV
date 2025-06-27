# data_processing.py
class EmotionDataProcessor:
    def __init__(self, max_frames=600):
        self.max_frames = max_frames
        # 使用列表存储情绪历史
        self.emotion_history = []

    def record_emotion(self, emotion):
        # 记录当前识别的情绪
        if len(self.emotion_history) >= self.max_frames:
            self.emotion_history.pop(0)  # 移除最旧的情绪

        self.emotion_history.append(emotion)
        print("Emotion recorded:", emotion)
        print(self.emotion_history)

    def get_emotion_trends(self):
        # 返回完整的情绪历史列表
        return self.emotion_history.copy()

    def update_history(self, new_emotion):
        # 直接添加新情绪
        self.record_emotion(new_emotion)