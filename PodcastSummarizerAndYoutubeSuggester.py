import os
import streamlit as st
import yt_dlp
import whisper
import spacy
from pydub import AudioSegment
from transformers import pipeline
from googleapiclient.discovery import build



# Set API Key (Replace with your YouTube API Key)
API_KEY = "AIzaSyAWQ-Q9PJxOwXirog5-3zV9_PvakwCKxh8"

def download_youtube_audio(url, output_path="downloads/"):
    """Downloads YouTube audio and converts it to MP3."""
    os.makedirs(output_path, exist_ok=True)
    output_template = os.path.join(output_path, "%(title)s.%(ext)s")
    
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': output_template,
        'quiet': True,
        'no_warnings': True
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        downloaded_file = os.path.join(output_path, f"{info['title']}.{info['ext']}")
    
    new_file_path = os.path.join(output_path, f"{info['title']}.mp3")
    audio = AudioSegment.from_file(downloaded_file)
    audio.export(new_file_path, format="mp3")
    os.remove(downloaded_file)  # Remove original file
    
    return new_file_path

def transcribe_audio(file_path):
    """Transcribes an audio file using Whisper."""
    model = whisper.load_model("base")  # Adjust model size as needed
    result = model.transcribe(file_path)
    return result["text"]

def summarize_text(text):
    """Summarizes the transcribed text."""
    summarizer = pipeline("summarization", model="google/long-t5-tglobal-base", device=-1)
    summary = summarizer(text, max_length=250, min_length=50, do_sample=False, num_beams=5)
    return summary[0]['summary_text']

def extract_keywords(text):
    """Extracts keywords from text using spaCy."""
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text)
    keywords = list(set(ent.text for ent in doc.ents))
    return keywords

def search_podcasts(keywords, max_results=5):
    """Searches for relevant podcasts on YouTube."""
    youtube = build("youtube", "v3", developerKey=API_KEY)
    query = " ".join(keywords) + " podcast"
    request = youtube.search().list(part="snippet", q=query, type="video", maxResults=max_results, videoDuration="long")
    response = request.execute()
    return [(item["snippet"]["title"], f"https://www.youtube.com/watch?v={item['id']['videoId']}") for item in response.get("items", [])]

# Streamlit UI
st.title("🎙️ Podcast Summarizer & YouTube Suggester")
st.markdown("Upload a podcast or provide a YouTube link to get a summary and related podcast suggestions!")

option = st.radio("Select Input Type:", ("Upload Audio File", "YouTube Link"))

if option == "Upload Audio File":
    uploaded_file = st.file_uploader("Upload an MP3 file", type=["mp3"])
    if uploaded_file:
        file_path = f"downloads/{uploaded_file.name}"
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        transcript = transcribe_audio(file_path)
        summary = summarize_text(transcript)
        keywords = extract_keywords(transcript)
        suggestions = search_podcasts(keywords)
        
        st.subheader("Podcast Summary:")
        st.write(summary)
        
        st.subheader("Suggested Podcasts:")
        for title, url in suggestions:
            st.markdown(f"- [{title}]({url})")

elif option == "YouTube Link":
    youtube_url = st.text_input("Enter YouTube URL:")
    if st.button("Process Video") and youtube_url:
        audio_file = download_youtube_audio(youtube_url)
        transcript = transcribe_audio(audio_file)
        summary = summarize_text(transcript)
        keywords = extract_keywords(transcript)
        suggestions = search_podcasts(keywords)
        
        st.subheader("Podcast Summary:")
        st.write(summary)
        
        st.subheader("Suggested Podcasts:")
        for title, url in suggestions:
            st.markdown(f"- [{title}]({url})")
