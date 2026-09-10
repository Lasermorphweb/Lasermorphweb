#!/usr/bin/env python3
"""
真正的懒加载修复脚本
- 将所有 video source 的 src 改为 data-src
- 移除所有 autoplay 属性
- 添加 data-lazy 标记
"""

import os
import re
from pathlib import Path
from html.parser import HTMLParser

class VideoLazyLoadFixer:
    """修复HTML中的视频懒加载"""
    
    def __init__(self):
        self.fixes_count = 0
        
    def fix_html(self, content):
        """修复HTML内容中的视频标签"""
        original = content
        
        # 1. 移除 video 标签的 autoplay 属性
        content = re.sub(
            r'<video([^>]*?)\s+autoplay([^>]*?)>',
            r'<video\1\2>',
            content,
            flags=re.IGNORECASE | re.DOTALL
        )
        
        # 2. 将 source 的 src 改为 data-src (针对视频)
        # 只处理在 video 标签内的 source
        def replace_source_src(match):
            source_tag = match.group(0)
            # 如果已经有 data-src，跳过
            if 'data-src=' in source_tag:
                return source_tag
            # 将 src 改为 data-src
            source_tag = re.sub(
                r'\bsrc=',
                'data-src=',
                source_tag
            )
            return source_tag
        
        # 查找所有 source 标签并替换
        content = re.sub(
            r'<source[^>]+type="video/mp4"[^>]*>',
            replace_source_src,
            content,
            flags=re.IGNORECASE
        )
        
        # 3. 为 video 标签添加 data-lazy 和 preload="none"
        def add_lazy_attrs(match):
            video_tag = match.group(0)
            # 如果已经有 data-lazy，跳过
            if 'data-lazy=' in video_tag:
                return video_tag
            # 如果已经有 preload，保留它，否则添加
            if 'preload=' not in video_tag:
                video_tag = video_tag.replace('<video', '<video preload="none"', 1)
            # 添加 data-lazy
            video_tag = video_tag.replace('<video', '<video data-lazy="true"', 1)
            return video_tag
        
        content = re.sub(
            r'<video(?![^>]*data-lazy=)[^>]*>',
            add_lazy_attrs,
            content,
            flags=re.IGNORECASE
        )
        
        # 4. 移除重复的属性
        content = re.sub(r'preload="none"\s+preload="none"', 'preload="none"', content)
        content = re.sub(r'data-lazy="true"\s+data-lazy="true"', 'data-lazy="true"', content)
        
        if content != original:
            self.fixes_count += 1
            
        return content

def process_file(file_path, fixer):
    """处理单个HTML文件"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        content = fixer.fix_html(content)
        
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        return False
    except Exception as e:
        print(f"✗ Error: {file_path} - {e}")
        return False

def main():
    root_path = Path('/Users/heshan3/Documents/Sponge')
    fixer = VideoLazyLoadFixer()
    
    # 查找所有HTML文件
    html_files = []
    for root, dirs, files in os.walk(root_path):
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        for file in files:
            if file.endswith('.html'):
                html_files.append(os.path.join(root, file))
    
    print("=" * 80)
    print("🔧 修复视频懒加载 - 真正阻止预加载")
    print("=" * 80)
    print()
    
    fixed_count = 0
    for html_file in html_files:
        rel_path = os.path.relpath(html_file, root_path)
        if process_file(html_file, fixer):
            print(f"✓ Fixed: {rel_path}")
            fixed_count += 1
    
    print()
    print("=" * 80)
    print(f"✅ 修复完成！")
    print(f"   修复文件数: {fixed_count}/{len(html_files)}")
    print()
    print("关键修改:")
    print("  1. 移除了所有 autoplay 属性")
    print("  2. 将 source src 改为 data-src")
    print("  3. 添加了 data-lazy 和 preload='none'")
    print()
    print("⚠️  重要提示:")
    print("  - 现在视频不会自动加载")
    print("  - 需要滚动到视频位置才会加载")
    print("  - 请在浏览器中测试验证")
    print("=" * 80)

if __name__ == '__main__':
    main()
