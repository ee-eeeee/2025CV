import os
import json
from PIL import Image
import argparse
from tqdm import tqdm

def fix_coco_image_dimensions(coco_json_path, images_dir, output_json_path=None):
    """
    补全COCO数据集中图片的长宽信息
    
    参数:
    coco_json_path (str): COCO标注JSON文件路径
    images_dir (str): 图片所在目录
    output_json_path (str, optional): 输出JSON文件路径，默认为None(覆盖原文件)
    """
    # 读取COCO JSON文件
    try:
        with open(coco_json_path, 'r', encoding='utf-8') as f:
            coco_data = json.load(f)
    except FileNotFoundError:
        print(f"错误: 文件 {coco_json_path} 不存在")
        return
    except json.JSONDecodeError:
        print(f"错误: 文件 {coco_json_path} 不是有效的JSON格式")
        return
    
    # 检查images字段是否存在
    if 'images' not in coco_data:
        print("错误: JSON文件中缺少'images'字段")
        return
    
    images = coco_data['images']
    updated_count = 0
    missing_path_count = 0
    
    # 遍历所有图片项
    for image in tqdm(images, desc="处理图片"):
        # 检查是否缺少width或height字段
        if 'width' not in image or 'height' not in image:
            file_name = image.get('file_name')
            if not file_name:
                print(f"警告: 图片项 {image.get('id')} 缺少'file_name'字段")
                missing_path_count += 1
                continue
            
            # 构建图片完整路径
            image_path = os.path.join(images_dir, file_name)
            
            # 检查图片文件是否存在
            if not os.path.exists(image_path):
                print(f"警告: 图片文件 {image_path} 不存在")
                missing_path_count += 1
                continue
            
            # 读取图片尺寸
            try:
                with Image.open(image_path) as img:
                    width, height = img.size
                    # 更新图片项
                    image['width'] = width
                    image['height'] = height
                    updated_count += 1
            except Exception as e:
                print(f"警告: 无法读取图片 {image_path} 的尺寸: {str(e)}")
    
    # 输出处理结果
    print(f"处理完成!")
    print(f"总共处理 {len(images)} 张图片")
    print(f"成功更新 {updated_count} 张图片的尺寸信息")
    print(f"找不到 {missing_path_count} 张图片的路径")
    
    # 保存更新后的JSON文件
    if output_json_path is None:
        output_json_path = coco_json_path
    
    try:
        with open(output_json_path, 'w', encoding='utf-8') as f:
            json.dump(coco_data, f, ensure_ascii=False, indent=2)
        print(f"更新后的JSON已保存到: {output_json_path}")
    except Exception as e:
        print(f"错误: 无法保存JSON文件: {str(e)}")

if __name__ == "__main__":
    # 创建命令行参数解析器
    parser = argparse.ArgumentParser(description='补全COCO数据集中图片的长宽信息')
    parser.add_argument('--json', required=True, help='COCO标注JSON文件路径')
    parser.add_argument('--images', required=True, help='图片所在目录')
    parser.add_argument('--output', help='输出JSON文件路径，默认为覆盖原文件')
    
    # 解析命令行参数
    args = parser.parse_args()
    
    # 执行补全操作
    fix_coco_image_dimensions(args.json, args.images, args.output)
