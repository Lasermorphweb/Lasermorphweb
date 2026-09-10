import subprocess
import os
from pathlib import Path

# 确保 ffmpeg 在 PATH 中
os.environ['PATH'] = '/opt/homebrew/bin:' + os.environ.get('PATH', '')

# ================= 配置区 =================
# 视频目录
VIDEO_DIR = Path("/Users/heshan3/Documents/Sponge/resources/surface_qualityvideo")

# 输出目录
OUTPUT_DIR = VIDEO_DIR / "compressed"

# 是否需要静音以减小体积
REMOVE_AUDIO = True
# ==========================================

def compress_video(input_path: Path, output_path: Path):
    """压缩单个视频，保持完整画面不裁剪"""
    cmd = [
        "ffmpeg",
        "-y",
        "-i", str(input_path),
        "-c:v", "libx264",
        "-crf", "28",
        "-preset", "slower",
        "-pix_fmt", "yuv420p",
        "-movflags", "+faststart",
        "-vf", "scale=trunc(iw/2)*2:trunc(ih/2)*2",  # 确保尺寸为偶数，不裁剪
    ]
    
    if REMOVE_AUDIO:
        cmd.append("-an")
        
    cmd.append(str(output_path))
    
    print(f"⏳ 正在压缩: {input_path.name}")
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print(f"  └─ ✅ 完成: {output_path.name}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"  └─ ❌ 失败: {e.stderr}")
        return False

def main():
    # 创建输出目录
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    # 获取所有 mp4 文件
    video_files = list(VIDEO_DIR.glob("*.mp4"))
    
    if not video_files:
        print(f"❌ 在 {VIDEO_DIR} 中未找到任何 .mp4 文件")
        return
    
    print(f"✅ 找到 {len(video_files)} 个视频文件")
    print(f"📁 输出目录: {OUTPUT_DIR}\n")
    
    success_count = 0
    for video_file in video_files:
        output_file = OUTPUT_DIR / video_file.name
        if compress_video(video_file, output_file):
            success_count += 1
    
    print(f"\n{'='*40}")
    print(f"处理完成: {success_count}/{len(video_files)} 个视频成功压缩")
    print(f"压缩后的视频位于: {OUTPUT_DIR}")

if __name__ == "__main__":
    main()
