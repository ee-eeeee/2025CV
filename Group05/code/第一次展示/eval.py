from ultralytics import YOLO
import torch


def validate_model():
    # 基本参数配置（对应命令行参数）
    config = {
        'model': 'runs/detect/train2/weights/best.pt',  # 训练好的模型路径
        'data': 'dataset/person.yaml',  # 数据集配置文件
        'device': 0 if torch.cuda.is_available() else 'cpu',  # 自动选择设备
        'batch': 4,  # 验证批量大小
        'task': 'detect',  # 任务类型
        'mode': 'val',  # 运行模式
        'save_json': True,  # 保存JSON格式结果
        'save_hybrid': True,  # 保存混合标签结果
        'plots': True  # 生成评估图表
    }

    # 初始化模型
    model = YOLO(config['model'])

    # 执行验证
    metrics = model.val(
        data=config['data'],
        device=config['device'],
        batch=config['batch'],
        task=config['task'],
        save_json=config['save_json'],
        save_hybrid=config['save_hybrid'],
        plots=config['plots']
    )

    # 打印关键指标
    print("\n=== 验证结果 ===")
    print(f"mAP@0.5: {metrics.box.map50:.4f}")
    print(f"mAP@0.5:0.95: {metrics.box.map:.4f}")

    # 返回完整指标字典
    return metrics


if __name__ == '__main__':
    # 检查GPU可用性
    print(f"CUDA可用: {torch.cuda.is_available()}")
    if torch.cuda.is_available():
        print(f"使用GPU: {torch.cuda.get_device_name(0)}")

    # 执行验证
    results = validate_model()