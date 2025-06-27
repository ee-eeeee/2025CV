import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

class EmotionVisualizer:
    def __init__(self):
        self.emotion_colors = {
            "others": "#1E90FF",  # 蓝色
            "happiness": "#FFD700",  # 金黄色
            "sadness": "#FF6347",  # 红色
            "surprise": "#808080",  # 灰色
            "disgust": "#00CED1",  # 青色
            "repression": "#90EE90",  # 浅绿色
            "fear": "#800080"   # 紫色
        }
        
        self.figure, self.ax = plt.subplots(figsize=(8, 0.5))
        self.canvas = None
        self.bars = []
        
    def initialize_canvas(self, parent_widget, tk):
        # 初始化matplotlib画布
        self.canvas = FigureCanvasTkAgg(self.figure, master=parent_widget)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # 创建空白情绪条
        self.create_empty_emotion_bar()
        
    def create_empty_emotion_bar(self):
        # 创建空白的情绪条
        self.ax.clear()
        self.bars = []
        self.ax.set_xlim(0, 600)
        self.ax.set_ylim(0, 1)
        self.ax.axis('off')
        self.canvas.draw()

    def update_emotion_bar(self, emotion_history):
        # 更新情绪条显示
        if not emotion_history:
            self.create_empty_emotion_bar()
            return

        self.ax.clear()
        self.ax.set_xlim(0, 600)
        self.ax.set_ylim(0, 1)
        self.ax.axis('off')

        # 合并连续相同的情绪
        segments = []
        current_emotion = emotion_history[0]
        current_count = 1

        for emotion in emotion_history[1:]:
            if emotion == current_emotion:
                current_count += 1
            else:
                segments.append((current_emotion, current_count))
                current_emotion = emotion
                current_count = 1

        segments.append((current_emotion, current_count))

        # 计算总持续时间（所有段的count总和）
        total_duration = sum(count for _, count in segments)

        # 计算每个情绪段应占的宽度（按持续时间比例）
        current_x = 0
        for emotion, count in segments:
            # 根据该段持续时间比例计算宽度
            segment_width = (count / total_duration) * 600

            # 绘制情绪条
            bar = self.ax.barh(0.5, segment_width, height=1, left=current_x,
                               color=self.emotion_colors.get(emotion, 'gray'))
            self.bars.append(bar)

            # 添加文字标注（显示情绪名称）
            self.ax.text(current_x + segment_width / 2, 0.5, emotion,
                         ha='center', va='center', color='white', fontsize=8)

            current_x += segment_width

        self.canvas.draw()

    def show_emotion_distribution(self, parent_widget, emotion_distribution):
        # 显示情绪分布饼图
        labels = list(emotion_distribution.keys())
        sizes = list(emotion_distribution.values())
        colors = [self.emotion_colors[label] for label in labels]
        
        fig, ax = plt.subplots(figsize=(6, 6))
        ax.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
        ax.axis('equal')  # 保证饼图是圆形
        
        canvas = FigureCanvasTkAgg(fig, master=parent_widget)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
    def show_emotion_trends(self, parent_widget, emotion_trends):
        # 显示情绪变化趋势图
        timestamps = np.arange(len(emotion_trends))
        colors = [self.emotion_colors.get(emotion, 'gray') for emotion in emotion_trends]
        
        fig, ax = plt.subplots(figsize=(8, 4))
        scatter = ax.scatter(timestamps, [1]*len(emotion_trends), c=colors, marker='s')
        
        # 添加颜色图例
        handles = [plt.Line2D([0], [0], marker='s', color='w', label=label,
                           markerfacecolor=color, markersize=10)
                  for label, color in self.emotion_colors.items()]
        
        ax.legend(handles=handles, loc='upper right')
        ax.set_xlabel('时间（帧）')
        ax.set_title('情绪变化趋势')
        
        canvas = FigureCanvasTkAgg(fig, master=parent_widget)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)