from ultralytics import YOLO

model = YOLO("yolov8n.pt")
if __name__ == '__main__':
    results = model.train(data="dataset/person.yaml", epochs=50, batch=8,device=0)             # 训练模型
