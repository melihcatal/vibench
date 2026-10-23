import os
import requests

# AssemblyAI Transcripts API - provide client utilities for Batch Speech-to-Text


def get_assemblyai_client():
    api_key = os.getenv("ASSEMBLYAI_API_KEY")
    if not api_key:
        raise RuntimeError("ASSEMBLYAI_API_KEY environment variable not set")
    return requests.Session(), api_key


# Request speaker diarization by enabling diarization in config


def diarize_meeting(session, api_key, audio_url):
    url = "https://api.assemblyai.com/v2/transcript"
    headers = {"Authorization": api_key, "Content-Type": "application/json"}
    payload = {
        "audio_url": audio_url,
        "config": {"diarization": True, "auto_punctuation": True, "format_text": True},
    }
    resp = session.post(url, json=payload, headers=headers)
    resp.raise_for_status()
    return resp.json()["id"]
