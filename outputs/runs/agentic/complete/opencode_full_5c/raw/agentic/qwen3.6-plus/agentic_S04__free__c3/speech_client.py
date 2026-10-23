import os
import requests
from typing import Optional

ASSEMBLYAI_API_BASE = "https://api.assemblyai.com/v2"
ASSEMBLYAI_MODEL = "assemblyai-2"


def get_assemblyai_api_key() -> str:
    api_key = os.environ.get("ASSEMBLYAI_API_KEY")
    if not api_key:
        raise ValueError("ASSEMBLYAI_API_KEY environment variable is not set")
    return api_key


def get_assemblyai_headers() -> dict:
    return {
        "authorization": get_assemblyai_api_key(),
        "content-type": "application/json",
    }


def create_assemblyai_session() -> requests.Session:
    session = requests.Session()
    session.headers.update(get_assemblyai_headers())
    session.base_url = ASSEMBLYAI_API_BASE
    return session


def upload_audio_file(session: requests.Session, audio_path: str) -> str:
    upload_url = f"{ASSEMBLYAI_API_BASE}/upload"
    with open(audio_path, "rb") as f:
        response = session.post(upload_url, data=f)
    response.raise_for_status()
    return response.json()["upload_url"]


def submit_transcription_job(
    session: requests.Session, audio_url: str, config: dict
) -> str:
    submit_url = f"{ASSEMBLYAI_API_BASE}/transcript"
    payload = {"audio_url": audio_url}
    payload.update(config)
    response = session.post(submit_url, json=payload)
    response.raise_for_status()
    return response.json()["id"]


def get_transcription_status(session: requests.Session, transcript_id: str) -> dict:
    status_url = f"{ASSEMBLYAI_API_BASE}/transcript/{transcript_id}"
    response = session.get(status_url)
    response.raise_for_status()
    return response.json()


def poll_until_complete(
    session: requests.Session,
    transcript_id: str,
    poll_interval: float = 3.0,
    max_attempts: int = 200,
) -> dict:
    import time

    for _ in range(max_attempts):
        result = get_transcription_status(session, transcript_id)
        status = result.get("status")
        if status == "completed":
            return result
        if status == "error":
            raise RuntimeError(f"Transcription failed: {result.get('error')}")
        time.sleep(poll_interval)
    raise TimeoutError(f"Transcription {transcript_id} did not complete within timeout")
