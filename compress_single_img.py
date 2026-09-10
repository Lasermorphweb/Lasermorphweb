import sys
import os
from PIL import Image

def compress_image(image_path):
    """
    压缩图片并直接替换原文件
    """
    # 检查文件是否存在
    if not os.path.isfile(image_path):
        print(f"❌ 错误：找不到文件 '{image_path}'")
        return

    try:
        # 获取压缩前的原始大小
        original_size = os.path.getsize(image_path)
        
        with Image.open(image_path) as img:
            img_format = img.format
            
            # 针对不同格式采取不同的压缩策略，直接覆盖原路径
            if img_format in ['JPEG', 'MPO']:
                # JPEG 支持调整质量 (quality)，范围 1-95，75 是清晰度和体积的极佳平衡点
                img.save(image_path, format='JPEG', optimize=True, quality=75)
            elif img_format == 'PNG':
                # PNG 是无损格式，optimize=True 会尝试优化其内部结构来减小体积
                img.save(image_path, format='PNG', optimize=True)
            elif img_format == 'WEBP':
                img.save(image_path, format='WEBP', optimize=True, quality=75)
            else:
                # 其他格式尝试默认优化
                img.save(image_path, optimize=True)

        # 获取压缩后的新大小
        new_size = os.path.getsize(image_path)
        
        # 打印压缩结果和体积变化
        print(f"✅ 压缩并替换成功: {image_path}")
        print(f"📉 体积变化: {original_size / 1024:.2f} KB  =>  {new_size / 1024:.2f} KB")

    except Exception as e:
        print(f"❌ 处理文件时发生错误: {e}")

if __name__ == "__main__":
    # 检查是否提供了路径参数
    if len(sys.argv) < 2:
        print("💡 用法: python compress_single.py <图片路径>")
        sys.exit(1)
        
    target_path = sys.argv[1]
    compress_image(target_path)