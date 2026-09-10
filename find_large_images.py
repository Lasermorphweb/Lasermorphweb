#!/usr/bin/env python3
"""
Find and list large images that need optimization
"""

import os
from pathlib import Path

def find_large_images(directory, min_size_mb=5):
    """Find images larger than min_size_mb megabytes"""
    large_images = []
    image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.webp', '.JPG', '.JPEG', '.PNG', '.GIF', '.WEBP'}
    
    for root, dirs, files in os.walk(directory):
        # Skip hidden directories
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        
        for file in files:
            if any(file.endswith(ext) for ext in image_extensions):
                file_path = os.path.join(root, file)
                file_size = os.path.getsize(file_path)
                size_mb = file_size / (1024 * 1024)
                
                if size_mb >= min_size_mb:
                    large_images.append((file_path, size_mb))
    
    return sorted(large_images, key=lambda x: x[1], reverse=True)

def main():
    root_path = Path('/Users/heshan3/Documents/Sponge')
    
    print("=" * 80)
    print("大图片文件列表（建议进一步压缩）")
    print("=" * 80)
    print()
    
    # Find images larger than 5MB
    large_images = find_large_images(root_path, min_size_mb=5)
    
    if not large_images:
        print("✓ 没有找到超过5MB的图片")
        return
    
    print(f"找到 {len(large_images)} 个超过5MB的图片：\n")
    
    total_size = 0
    for i, (file_path, size_mb) in enumerate(large_images, 1):
        rel_path = os.path.relpath(file_path, root_path)
        print(f"{i:2d}. {size_mb:6.2f} MB  {rel_path}")
        total_size += size_mb
    
    print()
    print("-" * 80)
    print(f"总计: {len(large_images)} 个文件，共 {total_size:.2f} MB")
    print()
    print("建议优化方案：")
    print("1. 使用 TinyPNG (https://tinypng.com/) 在线压缩")
    print("2. 使用 ImageOptim (macOS) 本地压缩")
    print("3. 转换为 WebP 格式（体积减少 25-35%）")
    print()
    
    # Export list to file
    output_file = root_path / 'large_images_list.txt'
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("需要优化的大图片列表\n")
        f.write("=" * 80 + "\n\n")
        for file_path, size_mb in large_images:
            rel_path = os.path.relpath(file_path, root_path)
            f.write(f"{size_mb:.2f} MB  {rel_path}\n")
        f.write(f"\n总计: {total_size:.2f} MB\n")
    
    print(f"✓ 已导出列表到: {output_file}")
    print()

if __name__ == '__main__':
    main()
