## Podcast Summarizer & YouTube Suggester ##

This repository implements a Streamlit-based application that transcribes, summarizes, and analyzes podcasts. Users can upload an audio file or provide a YouTube link, and the application will generate a summary and suggest related podcasts using YouTube's API.

## ** Project Overview ** ##

The objective of this project is to:

Extract audio from a podcast or YouTube video.

Transcribe the speech to text using OpenAI's Whisper model.

Generate a concise summary using a Transformer-based model.

Extract relevant keywords from the transcribed text.

Search YouTube for related podcast recommendations based on extracted keywords.

## ** Features ** ##

Audio Processing & Transcription

Converts YouTube videos into audio.

Supports MP3 file uploads.

Uses Whisper for high-quality speech-to-text conversion.

Summarization & Keyword Extraction

Summarizes long podcast transcripts using a Transformer model.

Extracts important keywords using spaCy NLP.

YouTube Podcast Recommendation

Searches for relevant podcasts on YouTube.

Uses Google API to suggest similar podcast videos.

User-Friendly Streamlit UI

Allows users to upload files or enter YouTube URLs.

Displays transcriptions, summaries, and suggested content.



