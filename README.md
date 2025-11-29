# 🎬 AI Video Generation Pipeline

Welcome to the **AI Video Generation Project** a modular pipeline that transforms text prompts into fully edited videos using AI for script generation, voice synthesis, media retrieval, and final video assembly.

This repository includes:

* 🔤 **Text Generation** (Gemini API)
* 🎤 **Text-to-Speech**
* 📸 **Pexels API Integration** (video/image search)
* 🎞️ **Automated Video Editor**
* 🚀 **Streamlit Demo App** to test the entire pipeline interactively

---

## 📁 Project Structure

Here’s a quick overview of the project layout:

```
project/
│
├── src/
│   ├── text_generation.py      # Gemini script generator
│   ├── text_to_speech.py       # AI voice generation
│   ├── pexels_api.py           # Fetch videos/images from Pexels
│   ├── video_editor.py         # Combine visuals + audio + transitions
│   ├── cleanup.py
│   └── list_models.py
│
│
├── demo.py                     # Streamlit app that ties everything together
├── requirements.txt
└── README.md
```

All core logic lives inside the `src/` folder, while the `demo.py` file provides a friendly interface to run the full pipeline.

---

## 🔐 Environment Variables

To run the project, create a `.env` file in the root directory.
This file is **not included** in the repo for security reasons.

Create `.env` and add the following:

```
PEXELS_API_KEY="your pexels api key"
GEMINI_API_KEY="your gemini api key"

# Optional settings
VIDEO_OUTPUT_DIR=data/output
VIDEO_DOWNLOAD_DIR=data/videos
AUDIO_OUTPUT_DIR=data/audio
SCRIPT_FOLDER=data/scripts
KEYWORDS_FOLDER=data/key_words
TARGET_VIDEO_DURATION=60
```

If these folders don’t exist, the project will create them automatically.

---

## ▶️ How to Run

### **1. Install dependencies**

```
pip install -r requirements.txt
```

### **2. Run the Streamlit Demo**

```
streamlit run demo.py
```

This launches a full UI where you can:

* Enter a topic
* Generate a script using Gemini
* Fetch visuals from Pexels
* Generate narration audio
* Render the final video

---

## ✨ Features

* 🔧 **Modular architecture** — swap or upgrade components easily
* 🤖 **AI-powered storytelling** using Gemini
* 🎧 **Natural-sounding**
* 📹 **Automated video composition** with transitions + background audio
* 🌐 **Streamlit interface** for rapid testing

---

## 🤝 Contributing

Pull requests are welcome! If you have ideas for improvements or want to add new features, feel free to open an issue.
