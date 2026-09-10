from moviepy import VideoFileClip
from moviepy.video.fx import Crop
from pathlib import Path

def crop_video_final():
    # 原始文件路径
    input_path = Path("/Users/heshan3/Documents/Sponge/resources/gif_designtool/morphing_compression.mp4")
    # 输出路径（直接覆盖之前的 _cropped 文件）
    output_path = input_path.with_name(f"{input_path.stem}_cropped.mp4")

    if not input_path.exists():
        print(f"错误：找不到原始文件 {input_path}")
        return

    # 加载视频
    clip = VideoFileClip(str(input_path))
    w, h = clip.size

    # --- 精准裁切数值调整 ---
    # 根据最新快照分析：
    # 左右黑边较厚，各需裁掉约 15%
    # 上下边框在之前的 13% 和 85% 基础上基本保持稳定
    
    x1 = int(w * 0.12)   # 左侧裁掉 15% (约 192px)
    x2 = int(w * 0.88)   # 右侧保留到 85% (约 1088px)
    y1 = int(h * 0.13)   # 顶部裁掉 13%
    y2 = int(h * 0.85)   # 底部保留到 85%

    print(f"执行最终裁切... 目标宽度: {x2-x1}px, 目标高度: {y2-y1}px")

    # 使用 MoviePy 2.0 的 Crop 类和 with_effects 方法
    cropped_clip = clip.with_effects([Crop(x1=x1, y1=y1, x2=x2, y2=y2)])
    
    # 执行导出（覆盖旧的 _cropped 文件）
    cropped_clip.write_videofile(
        str(output_path), 
        codec="libx264", 
        audio=True,
        temp_audiofile='temp-audio-final.m4a', 
        remove_temp=True
    )

    print(f"✨ 成功覆盖！干净的视频已保存至: {output_path}")

if __name__ == "__main__":
    crop_video_final()