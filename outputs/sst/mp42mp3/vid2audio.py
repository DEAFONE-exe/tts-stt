from moviepy import VideoFileClip
import os

def convert_mp4_to_mp3(mp4_path, mp3_path=None):
    if not os.path.isfile(mp4_path):
        print(f"❌ File not found: {mp4_path}")
        return

    if not mp3_path:
        mp3_path = os.path.splitext(mp4_path)[0] + ".mp3"

    try:
        print(f"🔄 Converting {mp4_path} to {mp3_path}...")
        video = VideoFileClip(mp4_path)
        video.audio.write_audiofile(mp3_path)
        print("✅ Conversion complete.")
    except Exception as e:
        print(f"⚠️ Error during conversion: {e}")

# Example usage

convert_mp4_to_mp3("example2.mp4")
