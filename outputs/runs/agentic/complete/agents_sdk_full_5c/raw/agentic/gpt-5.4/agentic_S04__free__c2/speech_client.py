from __future__ import annotations

import os
from typing import Any, Dict, Optional

import requests

ASSEMBLYAI_BASE_URL = "https://api.assemblyai.com/v2"
ASSEMBLYAI_API_KEY_ENV = "ASSEMBLYAI_API_KEY"


def get_api_key() -> str:
    api_key = os.getenv(ASSEMBLYAI_API_KEY_ENV)
    if not api_key:
        raise RuntimeError(f"Missing required environment variable: {ASSEMBLYAI_API_KEY_ENV}")
    return api_key


def build_headers(api_key: Optional[str] = None) -> Dict[str, str]:
    return {
        "authorization": api_key or get_api_key(),
        "content-type": "application/json",
    }


def create_session(api_key: Optional[str] = None) -> requests.Session:
    session = requests.Session()
    session.headers.update(build_headers(api_key))
    return session


def transcript_endpoint(transcript_id: Optional[str] = None) -> str:
    if transcript_id:
        return f"{ASSEMBLYAI_BASE_URL}/transcript/{transcript_id}"
    return f"{ASSEMBLYAI_BASE_URL}/transcript"


def raise_for_assemblyai_error(response: requests.Response) -> None:
    try:
        response.raise_for_status()
    except requests.HTTPError as exc:
        detail: Any
        try:
            detail = response.json()
        except Exception:
            detail = response.text
        raise RuntimeError(f"AssemblyAI request failed: {detail}") from exc
