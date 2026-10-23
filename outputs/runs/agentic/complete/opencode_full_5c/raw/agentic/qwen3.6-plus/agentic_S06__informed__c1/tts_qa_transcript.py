import os
import time
from typing import Optional
import httpx
from speech_models import (
    TranscriptRequest,
    TranscriptResponse,
    normalize_transcript_response,
)


ASSEMBLYAI_API_BASE = "https://api.assemblyai.com/v2"


def _get_assemblyai_key(api_key: Optional[str] = None) -> str:
    key = api_key or os.environ.get("ASSEMBLYAI_API_KEY")
    if not key:
        raise ValueError("ASSEMBLYAI_API_KEY environment variable is not set")
    return key


def _upload_audio(api_key: str, audio_file_path: str) -> str:
    headers = {"authorization": api_key}
    url = f"{ASSEMBLYAI_API_BASE}/upload"
    with open(audio_file_path, "rb") as f:
        audio_data = f.read()
    with httpx.Client(timeout=120.0) as client:
        response = client.post(url, headers=headers, content=audio_data)
        response.raise_for_status()
    return response.json().get("upload_url")


def _request_transcription(
    api_key: str, audio_url: str, language_code: str = "en"
) -> str:
    headers = {
        "authorization": api_key,
        "content-type": "application/json",
    }
    payload = {
        "audio_url": audio_url,
        "language_code": language_code,
    }
    url = f"{ASSEMBLYAI_API_BASE}/transcript"
    with httpx.Client(timeout=30.0) as client:
        response = client.post(url, headers=headers, json=payload)
        response.raise_for_status()
    return response.json().get("id")


def _poll_transcription(
    api_key: str,
    transcript_id: str,
    poll_interval: float = 3.0,
    max_wait: float = 300.0,
) -> dict:
    headers = {"authorization": api_key}
    url = f"{ASSEMBLYAI_API_BASE}/transcript/{transcript_id}"
    elapsed = 0.0
    with httpx.Client(timeout=30.0) as client:
        while elapsed < max_wait:
            response = client.get(url, headers=headers)
            response.raise_for_status()
            data = response.json()
            status = data.get("status")
            if status == "completed":
                return data
            if status == "error":
                raise RuntimeError(
                    f"AssemblyAI transcription failed: {data.get('error')}"
                )
            time.sleep(poll_interval)
            elapsed += poll_interval
    raise TimeoutError(f"AssemblyAI transcription timed out after {max_wait}s")


def transcribe_qa_sample(
    audio_file_path: str,
    language_code: str = "en",
    model: str = "assemblyai_default",
    api_key: Optional[str] = None,
) -> TranscriptResponse:
    key = _get_assemblyai_key(api_key)
    audio_url = _upload_audio(key, audio_file_path)
    transcript_id = _request_transcription(key, audio_url, language_code)
    raw = _poll_transcription(key, transcript_id)
    return normalize_transcript_response(raw)


def transcribe_qa_sample_from_url(
    audio_url: str,
    language_code: str = "en",
    api_key: Optional[str] = None,
) -> TranscriptResponse:
    key = _get_assemblyai_key(api_key)
    transcript_id = _request_transcription(key, audio_url, language_code)
    raw = _poll_transcription(key, transcript_id)
    return normalize_transcript_response(raw)
