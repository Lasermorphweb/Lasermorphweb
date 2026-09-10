import subprocess
from pathlib import Path

# ================= 配置区 =================

# 你的工作目录路径
BASE_DIR = Path("/Users/heshan3/Documents/Sponge/resources/gif_designtool")
# 自动在目标路径下创建的 gif 文件夹
OUTPUT_DIR = BASE_DIR / "gif"

# 裁剪参数：去除底部 50 像素的任务栏
# 公式说明：in_w(原宽) : in_h-50(原高减去50) : 0(X轴起点) : 0(Y轴起点)
CROP_BOTTOM_PIXELS = 50
CROP_FILTER = f"crop=in_w:in_h-{CROP_BOTTOM_PIXELS}:0:0"

# 网页优化参数
# fps=15：降低帧率以减小 GIF 体积 (网页端15帧已经足够流畅)
# scale=1080:-1：将宽度等比缩放到 1080px (如果原视频很大，这能极大缩减 GIF 体积)
FPS = 15
SCALE_WIDTH = 1080
OPTIMIZATION_FILTER = f"fps={FPS},scale={SCALE_WIDTH}:-1:flags=lanczos"

# ================= 逻辑区 =================

def main():
    # 确保输出目录存在
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # 获取所有 mp4 文件
    mp4_files = list(BASE_DIR.glob("*.mp4"))
    
    if not mp4_files:
        print("❌ 在指定目录下没有找到 .mp4 文件，请检查路径。")
        return

    print(f"✅ 找到 {len(mp4_files)} 个视频，开始处理并裁剪底部 {CROP_BOTTOM_PIXELS}px...")

    for video_path in mp4_files:
        output_path = OUTPUT_DIR / f"{video_path.stem}.gif"
        
        # 构建高级视频滤镜链 (生成局部专属调色板，画质更好)
        vf_string = f"{CROP_FILTER},{OPTIMIZATION_FILTER},split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse"
        
        cmd = [
            "ffmpeg",
            "-y",                   # 强制覆盖已存在的文件
            "-i", str(video_path),   # 输入文件
            "-vf", vf_string,        # 视频滤镜
            str(output_path)         # 输出文件
        ]
        
        print(f"⏳ 正在转换: {video_path.name} ...")
        
        # 运行 ffmpeg 命令，隐藏终端长篇大论的输出日志
        try:
            subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            print(f"  └─ ✨ 成功! 已保存至 gif/{output_path.name}")
        except subprocess.CalledProcessError:
            print(f"  └─ ❌ 转换失败: {video_path.name}")

    print("\n🎉 所有视频处理完毕！请前往 gif 文件夹查看。")

if __name__ == "__main__":
    main()