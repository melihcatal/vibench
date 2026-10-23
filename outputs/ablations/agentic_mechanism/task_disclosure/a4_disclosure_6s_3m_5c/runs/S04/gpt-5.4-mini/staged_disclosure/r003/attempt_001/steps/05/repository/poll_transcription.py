import os
import time
from typing import Any, Dict

import requests


ASSEMBLYAI_API_BASE = "https://api.assemblyai.com/v2"


def _headers() -> Dict[str, str]:
    api_key = os.environ.get("ASSEMBLYAI_API_KEY")
    if not api_key:
        raise ValueError("ASSEMBLYAI_API_KEY is required")
    return {"authorization": api_key, "content-type": "application/json"}


def _get_transcript(transcript_id: str) -> Dict[str, Any]:
    response = requests.get(f"{ASSEMBLYAI_API_BASE}/transcript/{transcript_id}", headers=_headers(), timeout=30)
    response.raise_for_status()
    return response.json()


def poll_transcription(transcript_id: str, interval_seconds: float = 3.0, timeout_seconds: float = 600.0) -> str:
    start = time.time()
    while True:
        data = _get_transcript(transcript_id)
        status = data.get("status")
        if status == "completed":
            return data.get("text", "")
        if status == "error":
            raise RuntimeError(data.get("error", "transcription failed"))
        if time.time() - start > timeout_seconds:
            raise TimeoutError("timed out waiting for transcription")
        time.sleep(interval_seconds)
