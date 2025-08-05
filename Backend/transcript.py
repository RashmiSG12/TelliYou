# from urllib.parse import urlparse, parse_qs
# from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound, VideoUnavailable
# # from pytube import YouTube

# def extract_video_id(url):
#     parsed_url = urlparse(url)
#     if parsed_url.hostname in ["youtu.be"]:
#         return parsed_url.path[1:]
#     elif parsed_url.hostname in ["www.youtube.com", "youtube.com"]:
#         if parsed_url.path == "/watch":
#             return parse_qs(parsed_url.query).get("v", [None])[0]
#         elif parsed_url.path.startswith("/embed/"):
#             return parsed_url.path.split("/embed/")[1]
#     return None

# def fetch_transcript(video_id: str) -> str:
#     try:
#         transcript_list = YouTubeTranscriptApi.get_transcript(video_id, languages=["en"])
#         transcript = " ".join(chunk["text"] for chunk in transcript_list)
#         print("Transcript loaded.")
#         return transcript
#     except TranscriptsDisabled:
#         print("No transcript available for this video.")
#         return None


import os
import webvtt
from yt_dlp import YoutubeDL
from urllib.parse import urlparse, parse_qs


def extract_video_id(url):
    parsed_url = urlparse(url)
    if parsed_url.hostname in ["youtu.be"]:
        return parsed_url.path[1:]
    elif parsed_url.hostname in ["www.youtube.com", "youtube.com"]:
        if parsed_url.path == "/watch":
            return parse_qs(parsed_url.query).get("v", [None])[0]
        elif parsed_url.path.startswith("/embed/"):
            return parsed_url.path.split("/embed/")[1]
    return None


def fetch_transcript(video_id: str) -> str:
    try:
        url = f"https://www.youtube.com/watch?v={video_id}"
        output_dir = "subtitles"
        os.makedirs(output_dir, exist_ok=True)

        ydl_opts = {
            'skip_download': True,
            'writesubtitles': True,
            'writeautomaticsub': True,
            'subtitleslangs': ['en'],
            'subtitlesformat': 'vtt',
            'outtmpl': os.path.join(output_dir, f"{video_id}.%(ext)s")
        }

        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        vtt_path = os.path.join(output_dir, f"{video_id}.en.vtt")
        if not os.path.exists(vtt_path):
            print("❌ Subtitle file not found.")
            return None

        full_text = ""
        for caption in webvtt.read(vtt_path):
            full_text += caption.text + " "

        return full_text.strip()

    except Exception as e:
        print(f"❌ Unexpected error in yt-dlp transcript fetching: {e}")
        return None



