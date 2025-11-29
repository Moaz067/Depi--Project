from typing import List, Dict, Any, Optional
import os
import re
import requests
from dotenv import load_dotenv
from datetime import datetime

# Load .env variables
load_dotenv()

PEXELS_API_KEY = os.getenv("PEXELS_API_KEY")
VIDEO_DOWNLOAD_DIR = os.getenv("VIDEO_DOWNLOAD_DIR", "data/videos")
DOWNLOADED_LINKS_FILE = os.path.join(VIDEO_DOWNLOAD_DIR, "downloaded_links.txt")

# Ensure the download folder exists
os.makedirs(VIDEO_DOWNLOAD_DIR, exist_ok=True)


def sanitize_filename(name: str) -> str:
    """Remove invalid characters for filenames"""
    return re.sub(r'[\\/*?:"<>|]', "", name.replace(" ", "_")).strip()


def is_already_downloaded(video_url: str) -> bool:
    """Check if a video was already downloaded"""
    if os.path.exists(DOWNLOADED_LINKS_FILE):
        with open(DOWNLOADED_LINKS_FILE, "r", encoding="utf-8") as f:
            return video_url in f.read()
    return False


def mark_as_downloaded(video_url: str) -> None:
    """Mark a video URL as downloaded"""
    with open(DOWNLOADED_LINKS_FILE, "a", encoding="utf-8") as f:
        f.write(video_url + "\n")


def choose_best_video_file(video: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Choose the best resolution video file from Pexels response"""
    files = video.get("video_files", [])
    if not files:
        return None
    # Pick the file with largest width × height
    best = max(files, key=lambda f: f.get("width", 0) * f.get("height", 0))
    return best


def search_videos(query: str, max_results: int = 5) -> List[Dict[str, Any]]:
    """Search videos on Pexels by keyword"""
    url = f"https://api.pexels.com/videos/search?query={query}&per_page={max_results}"
    headers = {"Authorization": PEXELS_API_KEY}
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"❌ Pexels API error: {response.status_code} - {response.text}")
        return []
    return response.json().get("videos", [])


def download_video(video: Dict[str, Any], output_dir: str = VIDEO_DOWNLOAD_DIR) -> Optional[str]:
    """Download the best quality video from Pexels"""
    os.makedirs(output_dir, exist_ok=True)

    video_file = choose_best_video_file(video)
    if not video_file:
        print("❌ No video files found.")
        return None

    video_url = video_file["link"]
    if is_already_downloaded(video_url):
        print(f"⚠️ Skipping (already downloaded): {video_url}")
        return None

    raw_title = video.get("alt", f"pexels_video_{datetime.now().strftime('%H%M%S')}")
    filename = sanitize_filename(raw_title) + ".mp4"
    file_path = os.path.join(output_dir, filename)

    try:
        response = requests.get(video_url, stream=True)
        response.raise_for_status()
        with open(file_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

        mark_as_downloaded(video_url)
        print(f"✅ Downloaded: {file_path}")
        return file_path
    except Exception as e:
        print(f"❌ Download failed for {filename}: {e}")
        return None


if __name__ == "__main__":
    # Simple test
    keyword = input("Enter a keyword to search Pexels videos: ")
    videos = search_videos(keyword, max_results = 5)
    if videos:
        num_to_download = 5
        for video in videos[:num_to_download]:
            download_video(video)
    else:
        print("No videos found.")