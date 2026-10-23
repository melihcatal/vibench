from __future__ import annotations

import os
from typing import Any, Dict, Optional

import requests

ASSEMBLYAI_BASE_URL = "https://api.assemblyai.com/v2"
ASSEMBLYAI_DEFAULT_POLL_SECONDS = 3.0


def get_assemblyai_api_key(explicit_api_key: Optional[str] = None) -> str:
    api_key = explicit_api_key or os.getenv("ASSEMBLYAI_API_KEY")
    if not api_key:
        raise ValueError("ASSEMBLYAI_API_KEY is required")
    return api_key


def build_assemblyai_headers(api_key: Optional[str] = None) -> Dict[str, str]:
    token = get_assemblyai_api_key(api_key)
    return {
        "authorization": token,
        "content-type": "application/json",
    }


def build_assemblyai_session(api_key: Optional[str] = None) -> requests.Session:
    session = requests.Session()
    session.headers.update(build_assemblyai_headers(api_key))
    return session


def submit_assemblyai_transcript(
    audio_url: str,
    *,
    api_key: Optional[str] = None,
    speech_model: str = "best",
    speaker_labels: bool = False,
    language_code: Optional[str] = None,
    word_boost: Optional[list[str]] = None,
) -> Dict[str, Any]:
    payload: Dict[str, Any] = {
        "audio_url": audio_url,
        "speech_model": speech_model,
        "speaker_labels": speaker_labels,
    }
    if language_code:
        payload["language_code"] = language_code
    if word_boost:
        payload["word_boost"] = word_boost
    session = build_assemblyai_session(api_key)
    response = session.post(f"{ASSEMBLYAI_BASE_URL}/transcript", json=payload, timeout=60)
    response.raise_for_status()
    return response.json()


def get_assemblyai_transcript(transcript_id: str, *, api_key: Optional[str] = None) -> Dict[str, Any]:
    session = build_assemblyai_session(api_key)
    response = session.get(f"{ASSEMBLYAI_BASE_URL}/transcript/{transcript_id}", timeout=60)
    response.raise_for_status()
    return response.json()
