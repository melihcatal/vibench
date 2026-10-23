import os
from typing import Any, Dict, Optional

import requests


ASSEMBLYAI_API_BASE = "https://api.assemblyai.com/v2"


class DiarizedTranscriptError(RuntimeError):
    pass


def _api_key(api_key: Optional[str] = None) -> str:
    key = api_key or os.getenv("ASSEMBLYAI_API_KEY")
    if not key:
        raise DiarizedTranscriptError("Missing ASSEMBLYAI_API_KEY")
    return key


def _headers(api_key: str) -> Dict[str, str]:
    return {"authorization": api_key, "content-type": "application/json"}


def request_speaker_diarization(
    audio_url: str,
    api_key: Optional[str] = None,
    language_code: Optional[str] = None,
    speech_model: Optional[str] = None,
    webhook_url: Optional[str] = None,
) -> Dict[str, Any]:
    key = _api_key(api_key)
    payload: Dict[str, Any] = {
        "audio_url": audio_url,
        "speaker_labels": True,
    }
    if language_code is not None:
        payload["language_code"] = language_code
    if speech_model is not None:
        payload["speech_model"] = speech_model
    if webhook_url is not None:
        payload["webhook_url"] = webhook_url

    response = requests.post(
        f"{ASSEMBLYAI_API_BASE}/transcript",
        headers=_headers(key),
        json=payload,
        timeout=30,
    )
    response.raise_for_status()
    return response.json()
