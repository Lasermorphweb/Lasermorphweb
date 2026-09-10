#!/usr/bin/env python3
"""
Batch optimize HTML files for faster loading
- Add lazy loading script to all pages
- Add loading="lazy" to images
- Optimize video loading
"""

import os
import re
from pathlib import Path

def add_lazy_load_script(html_content, depth_from_root):
    """Add lazy-load.js script to HTML head"""
    # Calculate relative path to lazy-load.js
    lazy_load_path = '../' * depth_from_root + 'js/lazy-load.js'
    
    # Check if lazy-load.js is already included
    if 'lazy-load.js' in html_content:
        return html_content
    
    # Find the position after the last Google Fonts link
    pattern = r'(</style>)'
    if re.search(pattern, html_content):
        # Find head section and add script before </head>
        head_pattern = r'(</head>)'
        script_tag = f'<script src="{lazy_load_path}"></script>\n    '
        html_content = re.sub(head_pattern, script_tag + r'\1', html_content, count=1)
    
    return html_content

def add_lazy_loading_to_images(html_content):
    """Add loading='lazy' to img tags that don't have it"""
    # Find img tags without loading attribute
    pattern = r'<img(?![^>]*loading=)([^>]*?)>'
    
    def add_loading(match):
        img_tag = match.group(0)
        # Don't add lazy loading to images in preload or with specific classes
        if 'preload' in img_tag or 'intro-img' in img_tag:
            return img_tag
        return img_tag.replace('<img', '<img loading="lazy"', 1)
    
    html_content = re.sub(pattern, add_loading, html_content)
    return html_content

def optimize_videos(html_content):
    """Add preload='none' to video tags"""
    # Find video tags and ensure they have preload='none'
    pattern = r'<video([^>]*?)>'
    
    def add_preload(match):
        video_attrs = match.group(1)
        if 'preload=' in video_attrs:
            return match.group(0)
        return f'<video preload="none"{video_attrs}>'
    
    html_content = re.sub(pattern, add_preload, html_content)
    return html_content

def get_depth_from_root(file_path, root_path):
    """Calculate the depth of a file from the root directory"""
    rel_path = os.path.relpath(file_path, root_path)
    return rel_path.count(os.sep)

def process_html_file(file_path, root_path):
    """Process a single HTML file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Calculate depth from root
        depth = get_depth_from_root(file_path, root_path)
        
        # Apply optimizations
        content = add_lazy_load_script(content, depth)
        content = add_lazy_loading_to_images(content)
        content = optimize_videos(content)
        
        # Only write if content changed
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✓ Optimized: {file_path}")
            return True
        else:
            print(f"  Skipped: {file_path} (no changes needed)")
            return False
    except Exception as e:
        print(f"✗ Error processing {file_path}: {e}")
        return False

def main():
    """Main function to process all HTML files"""
    root_path = Path('/Users/heshan3/Documents/Sponge')
    
    # Find all HTML files
    html_files = []
    for root, dirs, files in os.walk(root_path):
        # Skip hidden directories and node_modules
        dirs[:] = [d for d in dirs if not d.startswith('.') and d != 'node_modules']
        for file in files:
            if file.endswith('.html'):
                html_files.append(os.path.join(root, file))
    
    print(f"Found {len(html_files)} HTML files to process\n")
    
    optimized_count = 0
    for html_file in html_files:
        if process_html_file(html_file, root_path):
            optimized_count += 1
    
    print(f"\n✓ Optimization complete!")
    print(f"  Total files: {len(html_files)}")
    print(f"  Optimized: {optimized_count}")
    print(f"  Skipped: {len(html_files) - optimized_count}")

if __name__ == '__main__':
    main()
