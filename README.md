# 🎙️ Podcast Summarizer & YouTube Suggester
**A Streamlit-based web application that allows users to upload a podcast audio file or provide a YouTube link to get a summary, keyword extraction, and relevant podcast suggestions. The project leverages AI-powered speech-to-text, NLP, and summarization models to deliver concise podcast insights.**

## Features
🎧 Podcast & YouTube Audio Processing

### Upload an MP3 file or provide a YouTube link.
Uses yt_dlp to download and convert YouTube audio.
### 📝 AI-Based Transcription

Uses OpenAI’s Whisper model to transcribe the audio.
### 📜 Summarization

Summarizes the podcast using the Google Long-T5 model.
### 🔍 Keyword Extraction & Podcast Recommendations

Extracts key topics using spaCy.
Searches for related long-form podcasts on YouTube using the YouTube API.
### 🔊 Text-to-Speech (TTS) Playback

Uses Deepgram TTS API to convert the summary into speech.
Plays the summary audio using ffplay.
🎨 User-Friendly Web Interface

**Built using Streamlit for an interactive UI.**

## 🛠️ Installation & Setup
```
1️⃣ Clone the Repository
git clone https://github.com/absarraashid3/PodcastSummarizerAndYoutubeSuggester.git
cd PodcastSummarizerAndYoutubeSuggester

2️⃣ Install Dependencies
Ensure you have Python 3.8+ installed. Then run:
pip install -r requirements.txt

3️⃣ Install SpaCy Model
python3 -m spacy download en_core_web_sm

4️⃣ Set API Keys
Create a .env file in the project root and add:
YOUTUBE_API_KEY=your_youtube_api_key_here
DEEPGRAM_API_KEY=your_deepgram_api_key_here

5️⃣ Run the Application
python -m streamlit run PodcastSummarizerAndYoutubeSuggester.py

```
## 🖥️ Usage
### 1️⃣ Launch the app using the command above.
### 2️⃣ Select an input type:

**Upload an MP3 file.**
**Enter a YouTube URL.**
### 3️⃣ Get the transcript & summary.
### 4️⃣ View suggested podcasts based on extracted keywords.
### 5️⃣ Listen to the summary via text-to-speech.

## 📦 Project Structure
```
📂 PodcastSummarizerAndYoutubeSuggester/
├── 📜 requirements.txt
├── 📜 PodcastSummarizerAndYoutubeSuggester.py
├── 📂 downloads/ (stores downloaded audio files)
├── 📂 models/ (stores NLP models if needed)
└── 📜 README.md
```

## 🛠️ Tech Stack
```
Python
Streamlit (Frontend UI)
Whisper AI (Speech-to-Text)
spaCy (Keyword Extraction)
Hugging Face Transformers (Summarization Model)
YouTube API (Podcast Search)
Deepgram API (Text-to-Speech)
pydub (Audio Processing)
```

## 🔥 Future Enhancements
**✅ Improve multi-language support for transcriptions.**
**✅ Add user preferences for podcast recommendations.**
**✅ Enhance UI/UX with better design.**


## 📩 Contact
For queries, reach out via:

**Email: absarrashid3@gmail.com**

