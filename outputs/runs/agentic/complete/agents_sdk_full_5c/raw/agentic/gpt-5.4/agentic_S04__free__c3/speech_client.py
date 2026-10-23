from __future__ import annotations

import os
from typing import Any, Dict, Optional

import requests

ASSEMBLYAI_BASE_URL = "https://api.assemblyai.com/v2"
ASSEMBLYAI_API_KEY_ENV = "ASSEMBLYAI_API_KEY"


def get_api_key(api_key: Optional[str] = None) -> str:
    key = api_key or os.getenv(ASSEMBLYAI_API_KEY_ENV)
    if not key:
        raise ValueError(f"Missing API key in argument or environment variable {ASSEMBLYAI_API_KEY_ENV}")
    return key


def build_headers(api_key: Optional[str] = None) -> Dict[str, str]:
    return {
        "authorization": get_api_key(api_key),
        "content-type": "application/json",
    }


def submit_transcript_request(payload: Dict[str, Any], api_key: Optional[str] = None) -> Dict[str, Any]:
    response = requests.post(
        f"{ASSEMBLYAI_BASE_URL}/transcript",
        json=payload,
        headers=build_headers(api_key),
        timeout=60,
    )
    response.raise_for_status()
    return response.json()


def get_transcript(transcript_id: str, api_key: Optional[str] = None) -> Dict[str, Any]:
    response = requests.get(
        f"{ASSEMBLYAI_BASE_URL}/transcript/{transcript_id}",
        headers=build_headers(api_key),
        timeout=60,
    )
    response.raise_for_status()
    return response.json()
