import os
import requests

# AssemblyAI Transcripts API - provide client utilities for Batch Speech-to-Text


def get_assemblyai_client():
    api_key = os.getenv("ASSEMBLYAI_API_KEY")
    if not api_key:
        raise RuntimeError("ASSEMBLYAI_API_KEY environment variable not set")
    return requests.Session(), api_key


# Request timestamps by enabling timestamping in config


def timestamped_transcript(session, api_key, transcript_id):
    # First ensure transcription completed
    data = poll_transcription(session, api_key, transcript_id)
    if data["status"] != "completed":
        raise RuntimeError("Transcription not completed")
    # Retrieve full transcript with timestamps
    url = f"https://api.assemblyai.com/v2/transcript/{transcript_id}"
    headers = {"Authorization": api_key}
    resp = session.get(url, headers=headers)
    resp.raise_for_status()
    full_data = resp.json()
    words = full_data.get("words", [])
    # Build list of (word, start_sec, end_sec)
    timestamped = []
    for w in words:
        ts = w.get("start")
        te = w.get("end")
        timestamped.append({"text": w.get("text"), "start_sec": ts, "end_sec": te})
    return timestamped


# Helper reuse poll_transcription from earlier file
from poll_transcription import poll_transcription
