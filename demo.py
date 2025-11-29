from src.pexels_api import search_videos, download_video
from src.cleanup import clear_video_folder
import streamlit as st
from src.text_generator import generate_voice_over_script
from src.text_to_speech import text_to_speech
from src.video_editor import merge_videos_and_add_voiceover
import os
from datetime import datetime

st.title("Video Maker Demo")

# -------------------------
# SESSION STATE INITIALIZATION
# -------------------------
if "step" not in st.session_state:
    st.session_state.step = 1
if "script" not in st.session_state:
    st.session_state.script = ""
if "audio_path" not in st.session_state:
    st.session_state.audio_path = ""
if "video_path" not in st.session_state:
    st.session_state.video_path = ""
if "saved_prompt" not in st.session_state:
    st.session_state.saved_prompt = ""

prompt = st.text_input("Enter a topic for your video:")

# If user edits the prompt → reset workflow
if prompt != st.session_state.saved_prompt:
    st.session_state.step = 1
    st.session_state.script = ""
    st.session_state.audio_path = ""
    st.session_state.video_path = ""

# -------------------------
# STEP 1 — GENERATE SCRIPT
# -------------------------
if st.session_state.step == 1:
    if st.button("Generate Script"):
        if prompt.strip() == "":
            st.warning("Please enter a topic first.")
        else:
            with st.spinner("Generating script..."):
                st.session_state.script = generate_voice_over_script(prompt)
            st.session_state.saved_prompt = prompt
            st.success("Script generated!")
            st.session_state.step = 2
            st.rerun()

# Show script if generated
if st.session_state.script:
    st.subheader("Generated Script")
    st.write(st.session_state.script)

# -------------------------
# STEP 2 — GENERATE AUDIO
# -------------------------
if st.session_state.step >= 2:
    if st.button("Generate Audio"):
        os.makedirs("data/audio", exist_ok=True)
        with st.spinner("Generating audio..."):
            st.session_state.audio_path = text_to_speech(
                text=st.session_state.script
            )
        st.success("Audio generated!")
        st.session_state.step = 3
        st.rerun()

if st.session_state.audio_path:
    st.audio(st.session_state.audio_path)
    # st.write(f"Audio saved at: {st.session_state.audio_path}")

# -------------------------
# STEP 3 — GENERATE VIDEO
# -------------------------
if st.session_state.step >= 3:
    if st.button("Make Video"):
        
        # Clean old videos
        clear_video_folder("data/videos")
        
        # Download videos using Pexels
        with st.spinner("Searching & downloading videos..."):
            videos = search_videos(prompt, max_results=5)
            
            if not videos:
                st.error("No videos found for this topic on Pexels!")
                st.stop()
            
            for vid in videos:
                download_video(vid)  # saves into data/videos

        # Generate a unique filename for the output video
        ts = datetime.now().strftime('%Y%m%d_%H%M%S_%f')
        output_filename = f"video_{ts}.mp4"

        os.makedirs("data/final_videos", exist_ok=True)
        output_path = os.path.join("data/final_videos", output_filename)

        # Create the final video
        with st.spinner("Creating video..."):
            merge_videos_and_add_voiceover(
                videos_folder="data/videos",
                voiceover_path=st.session_state.audio_path,
                output_path=output_path,
                final_duration=60
            )

        # Store new video path
        st.session_state.video_path = output_path

        # Clear cache so Streamlit shows the correct video
        st.cache_data.clear()
        st.cache_resource.clear()

        st.success("Video created!")
        st.rerun()

# Display final video
if st.session_state.video_path:
    st.video(st.session_state.video_path)
    st.success("✅ Your video has been successfully created!")