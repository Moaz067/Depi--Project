import os
from moviepy.editor import VideoFileClip, AudioFileClip, concatenate_videoclips

def merge_videos_and_add_voiceover(
    videos_folder: str,
    voiceover_path: str,
    output_path: str,
    final_duration: int = 60
):
    print("[INFO] Loading videos...")

    video_files = [
        os.path.join(videos_folder, f)
        for f in os.listdir(videos_folder)
        if f.lower().endswith((".mp4", ".mov", ".mkv"))
    ]

    if not video_files:
        raise ValueError("No video files found in the folder.")

    video_files.sort()
    clips = [VideoFileClip(v) for v in video_files]

    print("[INFO] Concatenating videos...")
    merged = concatenate_videoclips(clips, method="compose")

    # --- LOAD AUDIO FIRST ---
    audio = AudioFileClip(voiceover_path)

    # --- DETERMINE FINAL DURATION ---
    if audio.duration < 60:
        final_duration = audio.duration
    else:
        final_duration = 60

    # --- TRIM AUDIO EXACTLY ---
    audio = audio.subclip(0, final_duration)

    print(f"Final duration will be {final_duration:.2f} seconds")

    # FIX VIDEO LENGTH BASED ON FINAL DURATION
    if merged.duration > final_duration:
        print("Trimming video...")
        merged = merged.subclip(0, final_duration)

    elif merged.duration < final_duration:
        print("Looping video to extend duration")
        loops = []
        current = 0

        while current < final_duration:
            for clip in clips:
                loops.append(clip)
                current += clip.duration
                if current >= final_duration:
                    break

        merged = concatenate_videoclips(loops, method="compose").subclip(0, final_duration)

    # --- SET AUDIO (NO set_duration!!!) ---
    final = merged.set_audio(audio)

    print("[INFO] Exporting video...")
    final.write_videofile(
        output_path,
        codec="libx264",
        audio_codec="aac",
        fps=24
    )

    print(f"[SUCCESS] Video saved at {output_path}")