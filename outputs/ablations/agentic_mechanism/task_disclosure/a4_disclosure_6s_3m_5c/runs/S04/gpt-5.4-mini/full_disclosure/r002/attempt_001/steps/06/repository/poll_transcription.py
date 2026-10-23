import os
import time
from typing import Any, Dict, Optional

import requests


ASSEMBLYAI_API_BASE = "https://api.assemblyai.com/v2"


class TranscriptionPollError(RuntimeError):
    pass


def _api_key(api_key: Optional[str] = None) -> str:
    key = api_key or os.getenv("ASSEMBLYAI_API_KEY")
    if not key:
        raise TranscriptionPollError("Missing ASSEMBLYAI_API_KEY")
    return key


def _headers(api_key: str) -> Dict[str, str]:
    return {"authorization": api_key}


def _get_json(url: str, headers: Dict[str, str]) -> Dict[str, Any]:
    response = requests.get(url, headers=headers, timeout=30)
    response.raise_for_status()
    return response.json()


def poll_transcription(
    transcription_id: str,
    api_key: Optional[str] = None,
    interval: float = 5.0,
    timeout: float = 600.0,
) -> Dict[str, Any]:
    key = _api_key(api_key)
    headers = _headers(key)
    url = f"{ASSEMBLYAI_API_BASE}/transcript/{transcription_id}"
    deadline = time.monotonic() + timeout

    while True:
        result = _get_json(url, headers)
        status = result.get("status")

        if status == "completed":
            return result
        if status == "error":
            raise TranscriptionPollError(result.get("error", "Transcription failed"))

        if time.monotonic() >= deadline:
            raise TranscriptionPollError("Timed out waiting for transcription to complete")

        time.sleep(interval)


def get_transcript_text(transcription_id: str, api_key: Optional[str] = None, **kwargs: Any) -> str:
    result = poll_transcription(transcription_id, api_key=api_key, **kwargs)
    return result.get("text", "")
