import subprocess
from pathlib import Path

# ================= 配置区 =================
# 将这里替换为你想要处理的【单个】MP4 文件的绝对路径
TARGET_FILE = Path("/Users/heshan3/Documents/Sponge/resources/designspace_morphing/morphing-Compression/morphing-Compression.mp4")

# 是否需要强制静音以进一步减小体积？(True 为静音，False 为保留原声)
REMOVE_AUDIO = True 
# ==========================================

def main():
    # 1. 基础校验
    if not TARGET_FILE.exists():
        print(f"❌ 找不到文件: {TARGET_FILE}")
        return
    if not TARGET_FILE.is_file():
        print(f"❌ 提供的路径是一个文件夹，请输入具体的文件路径。")
        return
    if TARGET_FILE.suffix.lower() != '.mp4':
        print(f"❌ 目标不是 .mp4 文件，请检查路径。")
        return

    print(f"✅ 锁定目标: {TARGET_FILE.name}，准备原地压缩替换...")

    # 2. 生成临时文件路径
    temp_path = TARGET_FILE.with_name(f"{TARGET_FILE.stem}_temp.mp4")
    
    # 3. 构建命令
    cmd = [
        "ffmpeg",
        "-y",
        "-i", str(TARGET_FILE),
        "-c:v", "libx264",         
        "-crf", "28",              
        "-preset", "slower",       
        "-pix_fmt", "yuv420p",     
        "-movflags", "+faststart", 
    ]
    
    # 如果配置为需要静音，则加上 -an 参数
    if REMOVE_AUDIO:
        cmd.append("-an")
        
    # 最后加上输出路径
    cmd.append(str(temp_path))
    
    print(f"⏳ 正在压缩，请稍候...")
    
    # 4. 执行并替换
    try:
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        temp_path.replace(TARGET_FILE)
        print(f"  └─ ✨ 处理完成！已成功覆盖原文件。")
        
    except subprocess.CalledProcessError:
        print(f"  └─ ❌ 压缩失败，原视频安全保留。")
        if temp_path.exists():
            temp_path.unlink()

if __name__ == "__main__":
    main()