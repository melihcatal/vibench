import os
import time
from typing import Any, Dict, Optional

import requests


ASSEMBLYAI_API_BASE = "https://api.assemblyai.com/v2"


def _headers() -> Dict[str, str]:
    api_key = os.getenv("ASSEMBLYAI_API_KEY")
    if not api_key:
        raise EnvironmentError("ASSEMBLYAI_API_KEY is required")
    return {"authorization": api_key, "content-type": "application/json"}


def _get_json(url: str) -> Dict[str, Any]:
    response = requests.get(url, headers=_headers(), timeout=30)
    response.raise_for_status()
    return response.json()


def poll_transcription(transcript_id: str, interval: float = 2.0, timeout: Optional[float] = 300.0) -> str:
    deadline = None if timeout is None else time.time() + timeout
    url = f"{ASSEMBLYAI_API_BASE}/transcript/{transcript_id}"
    while True:
        data = _get_json(url)
        status = data.get("status")
        if status == "completed":
            transcript = data.get("text")
            if transcript is None:
                raise RuntimeError("Transcript completed but no text was returned")
            return transcript
        if status == "error":
            raise RuntimeError(data.get("error", "Transcription failed"))
        if deadline is not None and time.time() > deadline:
            raise TimeoutError("Timed out waiting for transcription to complete")
        time.sleep(interval)
