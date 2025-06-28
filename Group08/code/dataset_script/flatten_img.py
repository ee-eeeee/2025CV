import os
import shutil
import argparse
from pathlib import Path
from tqdm import tqdm
from PIL import Image
import hashlib

def is_image_file(file_path):
    """检查文件是否为图片格式"""
    try:
        with Image.open(file_path) as img:
            img.verify()
        return True
    except Exception:
        return False

def flatten_images(source_dir, target_dir, move=False, keep_structure=False, overwrite=False, 
                   dry_run=False, create_log=False, ignore_duplicates=False):
    """
    将多层嵌套的图片文件平铺到单层目录
    
    参数:
    source_dir (str): 源目录路径
    target_dir (str): 目标目录路径
    move (bool): 是否移动文件而非复制
    keep_structure (bool): 是否保留部分目录结构（使用子文件夹名称作为前缀）
    overwrite (bool): 是否覆盖已存在的同名文件
    dry_run (bool): 是否只显示操作而不实际执行
    create_log (bool): 是否创建日志文件记录操作
    ignore_duplicates (bool): 是否忽略内容重复的文件
    """
    # 创建目标目录
    if not dry_run:
        os.makedirs(target_dir, exist_ok=True)
    
    # 初始化日志
    log = []
    duplicate_files = set()
    processed_files = 0
    skipped_files = 0
    duplicate_count = 0
    
    # 遍历所有子目录和文件
    for root, _, files in tqdm(os.walk(source_dir), desc="扫描目录"):
        for filename in files:
            source_path = os.path.join(root, filename)
            
            # 检查是否为图片文件
            if not is_image_file(source_path):
                continue
            
            # 构建目标文件名
            if keep_structure:
                # 使用子文件夹名称作为前缀
                subfolder = os.path.relpath(root, source_dir)
                subfolder_parts = subfolder.split(os.sep)
                prefix = "_".join(part for part in subfolder_parts if part)
                if prefix:
                    new_filename = f"{prefix}_{filename}"
                else:
                    new_filename = filename
            else:
                new_filename = filename
            
            # 处理同名文件
            target_path = os.path.join(target_dir, new_filename)
            if os.path.exists(target_path):
                if overwrite:
                    if ignore_duplicates:
                        # 检查文件内容是否相同
                        with open(source_path, 'rb') as f1, open(target_path, 'rb') as f2:
                            hash1 = hashlib.md5(f1.read()).hexdigest()
                            hash2 = hashlib.md5(f2.read()).hexdigest()
                            if hash1 == hash2:
                                duplicate_files.add(source_path)
                                duplicate_count += 1
                                log.append(f"忽略重复文件: {source_path} -> {target_path}")
                                continue
                    os.remove(target_path)
                else:
                    # 添加序号避免冲突
                    base, ext = os.path.splitext(new_filename)
                    counter = 1
                    while os.path.exists(os.path.join(target_dir, f"{base}_{counter}{ext}")):
                        counter += 1
                    target_path = os.path.join(target_dir, f"{base}_{counter}{ext}")
            
            # 记录操作
            log_entry = f"{'移动' if move else '复制'}: {source_path} -> {target_path}"
            log.append(log_entry)
            
            # 执行操作
            if not dry_run:
                try:
                    if move:
                        shutil.move(source_path, target_path)
                    else:
                        shutil.copy2(source_path, target_path)  # 保留元数据
                    processed_files += 1
                except Exception as e:
                    log_entry += f" (失败: {str(e)})"
                    log[-1] = log_entry
                    skipped_files += 1
    
    # 输出结果
    print("\n处理结果:")
    print(f"总处理文件数: {processed_files}")
    print(f"跳过文件数: {skipped_files}")
    print(f"检测到的重复文件数: {duplicate_count}")
    
    # 创建日志文件
    if create_log and log:
        log_path = os.path.join(target_dir, "flatten_images_log.txt")
        with open(log_path, 'w', encoding='utf-8') as f:
            f.write("\n".join(log))
        print(f"日志已保存到: {log_path}")
    
    # 列出重复文件（如果有）
    if duplicate_files and not dry_run:
        duplicates_log = os.path.join(target_dir, "duplicate_files.txt")
        with open(duplicates_log, 'w', encoding='utf-8') as f:
            f.write("\n".join(duplicate_files))
        print(f"重复文件列表已保存到: {duplicates_log}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='将多层嵌套的图片文件平铺到单层目录')
    parser.add_argument('--source', required=True, help='源目录路径')
    parser.add_argument('--target', required=True, help='目标目录路径')
    parser.add_argument('--move', action='store_true', help='移动文件而非复制')
    parser.add_argument('--keep-structure', action='store_true', help='保留部分目录结构（使用子文件夹名称作为前缀）')
    parser.add_argument('--overwrite', action='store_true', help='覆盖已存在的同名文件')
    parser.add_argument('--dry-run', action='store_true', help='只显示操作而不实际执行')
    parser.add_argument('--log', action='store_true', help='创建日志文件记录操作')
    parser.add_argument('--ignore-duplicates', action='store_true', help='忽略内容重复的文件')
    
    args = parser.parse_args()
    
    flatten_images(
        source_dir=args.source,
        target_dir=args.target,
        move=args.move,
        keep_structure=args.keep_structure,
        overwrite=args.overwrite,
        dry_run=args.dry_run,
        create_log=args.log,
        ignore_duplicates=args.ignore_duplicates
    )