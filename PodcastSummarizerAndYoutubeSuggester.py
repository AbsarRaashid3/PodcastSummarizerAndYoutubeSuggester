import os
import streamlit as st
import yt_dlp
import whisper
import spacy
from pydub import AudioSegment
from transformers import pipeline
from googleapiclient.discovery import build
import re
import requests
import subprocess

# Set environment variables
os.environ["TOKENIZERS_PARALLELISM"] = "false"

# Load NLP model
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    os.system("python -m spacy download en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")

# Set API Key (Replace with your YouTube API Key)
API_KEY = "AIzaSyAWQ-Q9PJxOwXirog5-3zV9_PvakwCKxh8"
DEEPGRAM_API_KEY = "6672021d942acd8ec7df300c71a6b9b56abf4d0b" # Replace with your actual key

# Initialize session state
if "summary" not in st.session_state:
    st.session_state.summary = None
if "suggestions" not in st.session_state:
    st.session_state.suggestions = None

def sanitize_filename(filename):
    return re.sub(r'[\\/*?:"<>|]', "", filename)

def download_youtube_audio(url, output_path="downloads/"):
    os.makedirs(output_path, exist_ok=True)
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': os.path.join(output_path, "%(id)s.%(ext)s"),
        'quiet': True,
        'no_warnings': True
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        downloaded_file = info["requested_downloads"][0]["filepath"]
    
    new_file_path = os.path.splitext(downloaded_file)[0] + ".mp3"
    if not downloaded_file.endswith(".mp3"):
        audio = AudioSegment.from_file(downloaded_file)
        audio.export(new_file_path, format="mp3")
        os.remove(downloaded_file)

    return new_file_path

def transcribe_audio(file_path):
    model = whisper.load_model("base")
    result = model.transcribe(file_path)
    return result["text"]

def summarize_text(text):
    summarizer = pipeline("summarization", model="google/long-t5-tglobal-base", device=-1)
    summary = summarizer(text, max_length=250, min_length=50, do_sample=False, num_beams=5)
    return summary[0]['summary_text']

def extract_keywords(text):
    doc = nlp(text)
    return list(set(ent.text for ent in doc.ents))

def search_podcasts(keywords, max_results=5):
    youtube = build("youtube", "v3", developerKey=API_KEY)
    query = " ".join(keywords) + " podcast"
    request = youtube.search().list(part="snippet", q=query, type="video", maxResults=max_results, videoDuration="long")
    response = request.execute()
    return [(item["snippet"]["title"], f"https://www.youtube.com/watch?v={item['id']['videoId']}") for item in response.get("items", [])]

class TextToSpeech:
    MODEL_NAME = "aura-helios-en"

    def __init__(self, deepgram_api_key):
        self.deepgram_api_key = deepgram_api_key
        self.process = None

    def speak(self, text):
        DEEPGRAM_URL = f"https://api.deepgram.com/v1/speak?model={self.MODEL_NAME}&encoding=linear16"
        headers = {"Authorization": f"Token {self.deepgram_api_key}", "Content-Type": "application/json"}
        payload = {"text": text}
        
        player_command = ["ffplay", "-autoexit", "-nodisp", "-"]
        self.process = subprocess.Popen(player_command, stdin=subprocess.PIPE)

        with requests.post(DEEPGRAM_URL, stream=True, headers=headers, json=payload) as r:
            for chunk in r.iter_content(chunk_size=1024):
                if chunk and self.process:
                    self.process.stdin.write(chunk)
                    self.process.stdin.flush()

        if self.process:
            self.process.stdin.close()
            self.process.wait()

    def stop(self):
        if self.process:
            self.process.terminate()
            self.process = None

# Initialize TTS
tts = TextToSpeech(DEEPGRAM_API_KEY)

st.title("🎙️ Podcast Summarizer & YouTube Suggester")
st.markdown("Upload a podcast or provide a YouTube link to get a summary and related podcast suggestions!")

option = st.radio("Select Input Type:", ("Upload Audio File", "YouTube Link"))

if option == "Upload Audio File":
    uploaded_file = st.file_uploader("Upload an MP3 file", type=["mp3"])
    if uploaded_file:
        file_path = f"downloads/{sanitize_filename(uploaded_file.name)}"
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        transcript = transcribe_audio(file_path)
        st.session_state.summary = summarize_text(transcript)
        keywords = extract_keywords(transcript)
        st.session_state.suggestions = search_podcasts(keywords)

if option == "YouTube Link":
    youtube_url = st.text_input("Enter YouTube URL:")
    if st.button("Process Video") and youtube_url:
        audio_file = download_youtube_audio(youtube_url)
        transcript = transcribe_audio(audio_file)
        st.session_state.summary = summarize_text(transcript)
        keywords = extract_keywords(transcript)
        st.session_state.suggestions = search_podcasts(keywords)

if st.session_state.summary:
    st.subheader("📜 Podcast Summary:")
    st.write(st.session_state.summary)

    if st.button("🔊 Hear Summary"):
        tts.speak(st.session_state.summary)
    if st.button("⏹️ Stop Audio"):
        tts.stop()

if st.session_state.suggestions:
    st.subheader("🎧 Suggested Podcasts:")
    for title, url in st.session_state.suggestions:
        st.markdown(f"- [{title}]({url})")
