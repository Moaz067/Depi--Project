from typing import List
import os
import re
from datetime import datetime
import google.genai as genai
from google.genai.types import HttpOptions
from dotenv import load_dotenv

# Load .env variables
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Configure Gemini client
client = genai.Client(api_key=GEMINI_API_KEY)

# Folder to save scripts and keywords
SCRIPT_FOLDER = os.getenv("SCRIPT_FOLDER", "data/scripts")
KEYWORDS_FOLDER = os.getenv("KEYWORDS_FOLDER", "data/key_words")

os.makedirs(SCRIPT_FOLDER, exist_ok=True)
os.makedirs(KEYWORDS_FOLDER, exist_ok=True)


def generate_voice_over_script(topic: str, lang: str = "en") -> str:
    prompt = f"""
    Write a 60-second voice-over script for a video on the following topic.
    The script should be natural, as if someone is reading it aloud.
    Start the script directly without any title.
    Keep it simple, professional, and in {lang}.

    Topic: {topic}
    """
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )
    return response.text.strip()


def save_script_to_txt(script: str, filename: str = None) -> str:
    if filename is None:
        filename = f"script_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    file_path = os.path.join(SCRIPT_FOLDER, filename)
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(script)
    print(f"✅ Script saved as {file_path}")
    return file_path


def extract_keywords(script: str, main_topic: str, num_keywords: int = 7) -> List[str]:
    prompt = f"""
    Extract exactly {num_keywords} clean keywords from the following text.
    Each keyword must include the word "{main_topic}".
    Do NOT include any explanation or numbering; return one keyword per line.

    Text:
    {script}
    """
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )
    keywords = [
        re.sub(r'^\d+[\).]?\s*', '', line.strip())
        for line in response.text.strip().split("\n")
        if line.strip()
    ]
    return keywords[:num_keywords]


def save_keywords(keywords: List[str], filename: str = None) -> str:
    if filename is None:
        filename = f"key_words_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    file_path = os.path.join(KEYWORDS_FOLDER, filename)
    with open(file_path, "w", encoding="utf-8") as f:
        f.write("\n".join(keywords))
    print(f"✅ Keywords saved as {file_path}")
    return file_path

# Simple test
if __name__ == "__main__":
    topic = input("Enter a topic for script generation: ")
    script = generate_voice_over_script(topic)
    save_script_to_txt(script)
    keywords = extract_keywords(script, topic)
    save_keywords(keywords)