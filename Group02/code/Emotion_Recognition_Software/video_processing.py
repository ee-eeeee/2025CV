import cv2
from emotion_recognition import EmotionRecognizer

class VideoProcessor:
    def __init__(self):
        self.video_path = None
        self.video_capture = None
        self.camera_capture = None
        self.emotion_recognizer = EmotionRecognizer()
        
    def load_video(self, file_path):
        self.video_path = file_path
        self.video_capture = cv2.VideoCapture(file_path)
        
    def open_camera(self):
        self.camera_capture = cv2.VideoCapture(0)
        
    def close_camera(self):
        if self.camera_capture:
            self.camera_capture.release()
            self.camera_capture = None
            
    def read_frame(self):
        if self.video_capture:
            ret, frame = self.video_capture.read()
            if ret:
                return frame
        return None
        
    def read_camera_frame(self):
        if self.camera_capture:
            ret, frame = self.camera_capture.read()
            if ret:
                # cv2.imwrite("G:\\1opencv\\a-software\\0raw.jpg", frame)
                return frame
        return None
        
    def process_frame(self, frames):

        emotion = self.emotion_recognizer.recognize_emotion(frames)

        return emotion

    def release_all(self):
        """释放所有资源"""
        if self.video_capture:
            self.video_capture.release()
            self.video_capture = None
        if self.camera_capture:
            self.camera_capture.release()
            self.camera_capture = None