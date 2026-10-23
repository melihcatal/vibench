import os
import requests

# AssemblyAI Transcripts API - provide client utilities for Batch Speech-to-Text


def get_assemblyai_client():
    api_key = os.getenv("ASSEMBLYAI_API_KEY")
    if not api_key:
        raise RuntimeError("ASSEMBLYAI_API_KEY environment variable not set")
    return requests.Session(), api_key


def submit_transcription(session, api_key, audio_url):
    url = "https://api.assemblyai.com/v2/transcript"
    headers = {"Authorization": api_key, "Content-Type": "application/json"}
    payload = {
        "audio_url": audio_url,
        "config": {"auto_punctuation": True, "format_text": True},
    }
    response = session.post(url, json=payload, headers=headers)
    response.raise_for_status()
    return response.json()["id"]


def poll_transcription(session, api_key, transcript_id):
    url = f"https://api.assemblyai.com/v2/transcript/{transcript_id}"
    headers = {"Authorization": api_key}
    while True:
        resp = session.get(url, headers=headers)
        resp.raise_for_status()
        data = resp.json()
        if data["status"] in ("completed", "error"):
            return data
        time.sleep(2)
