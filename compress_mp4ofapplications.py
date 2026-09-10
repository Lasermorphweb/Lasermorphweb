import subprocess
from pathlib import Path

# ================= 配置区 =================
# 你的目标视频主文件夹路径
TARGET_DIR = Path("/Users/heshan3/Documents/Sponge/resources/designspace_morphing")

# ================= 逻辑区 =================
def main():
    if not TARGET_DIR.exists():
        print(f"❌ 找不到文件夹: {TARGET_DIR}")
        return

    # 【关键修改】：使用 rglob 进行递归查找，穿透所有子文件夹
    mp4_files = list(TARGET_DIR.rglob("*.mp4"))
    
    # 过滤掉可能因为上次中断遗留的 _temp.mp4 文件
    mp4_files = [f for f in mp4_files if not f.name.endswith("_temp.mp4")]
    
    if not mp4_files:
        print("❌ 未在目标文件夹及其子文件夹中找到有效的 .mp4 文件。")
        return

    print(f"✅ 找到 {len(mp4_files)} 个视频，准备开始递归原地压缩替换...")
    print("⚠️ 提示：为了安全，脚本会先在文件同级目录生成临时文件，确认无误后再覆盖原文件。\n")

    for video_path in mp4_files:
        # 在原视频所在的当前子目录内创建一个临时文件路径
        temp_path = video_path.with_name(f"{video_path.stem}_temp.mp4")
        
        # 为了输出日志更清晰，获取相对于主文件夹的路径
        relative_path = video_path.relative_to(TARGET_DIR)
        
        cmd = [
            "ffmpeg",
            "-y",
            "-i", str(video_path),
            "-c:v", "libx264",         
            "-crf", "28",              
            "-preset", "slower",       
            "-pix_fmt", "yuv420p",     
            "-an",                     
            "-movflags", "+faststart", 
            str(temp_path)
        ]
        
        print(f"⏳ 正在压缩: {relative_path} ...")
        
        try:
            subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            
            # 压缩成功，直接用临时文件替换（覆盖）原文件
            temp_path.replace(video_path)
            
            print(f"  └─ ✨ 压缩成功，已覆盖原文件！")
            
        except subprocess.CalledProcessError:
            print(f"  └─ ❌ 压缩失败，原视频安全保留。")
            if temp_path.exists():
                temp_path.unlink()

    print("\n🎉 全部处理完毕！所有子文件夹中的视频已瘦身。")

if __name__ == "__main__":
    main()