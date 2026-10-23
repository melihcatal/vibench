import os
from pathlib import Path

# Helper utilities for speech-to-text workflows
# Define client configuration and common request/response handling

ASSEMBLYAI_API_KEY = os.getenv("ASSEMBLYAI_API_KEY")
if not ASSEMBLYAI_API_KEY:
    raise RuntimeError("ASSEMBLYAI_API_KEY not set")

BASE_URL = "https://api.assemblyai.com/v2"

# Normalize audio URL (ensure HTTPS) for request payloads


def normalize_audio_url(url: str) -> str:
    if not url.startswith("https://"):
        raise ValueError("Audio URL must use HTTPS")
    return url


# Create a reusable Requests session with timeout settings


def create_session() -> requests.Session:
    session = requests.Session()
    session.headers.update({"Content-Type": "application/json"})
    session.timeout = (5, 30)  # connect, read timeout
    return session


# Check transcription job status and return full JSON response


def check_job_status(session, transcript_id) -> dict:
    url = f"{BASE_URL}/transcript/{transcript_id}"
    resp = session.get(url, headers={"Authorization": ASSEMBLYAI_API_KEY})
    resp.raise_for_status()
    return resp.json()


# Simple wrapper to call the Transcription endpoint


def submit_transcript_job(session, audio_url: str, config=None) -> str:
    audio_url = normalize_audio_url(audio_url)
    payload = {"audio_url": audio_url, "config": config or {}}
    resp = session.post(
        f"{BASE_URL}/transcript",
        json=payload,
        headers={"Authorization": ASSEMBLYAI_API_KEY},
    )
    resp.raise_for_status()
    return resp.json()["id"]
