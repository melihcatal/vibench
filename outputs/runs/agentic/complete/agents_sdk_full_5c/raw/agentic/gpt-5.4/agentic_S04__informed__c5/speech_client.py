from __future__ import annotations

import os
from typing import Any, Dict, Optional

import requests

from speech_models import BatchTranscriptionRequest


ASSEMBLYAI_API_BASE = os.getenv("ASSEMBLYAI_API_BASE", "https://api.assemblyai.com/v2")
ASSEMBLYAI_API_KEY = os.getenv("ASSEMBLYAI_API_KEY")


def get_headers(api_key: Optional[str] = None) -> Dict[str, str]:
    token = api_key or ASSEMBLYAI_API_KEY
    if not token:
        raise ValueError("ASSEMBLYAI_API_KEY is required")
    return {
        "authorization": token,
        "content-type": "application/json",
    }


def submit_batch_transcription(request: BatchTranscriptionRequest, api_key: Optional[str] = None) -> Dict[str, Any]:
    response = requests.post(
        f"{ASSEMBLYAI_API_BASE}/transcript",
        headers=get_headers(api_key),
        json=request.to_assemblyai_payload(),
        timeout=60,
    )
    response.raise_for_status()
    return response.json()


def get_transcription(transcript_id: str, api_key: Optional[str] = None) -> Dict[str, Any]:
    response = requests.get(
        f"{ASSEMBLYAI_API_BASE}/transcript/{transcript_id}",
        headers=get_headers(api_key),
        timeout=60,
    )
    response.raise_for_status()
    return response.json()


def get_sentences(transcript_id: str, api_key: Optional[str] = None) -> Dict[str, Any]:
    response = requests.get(
        f"{ASSEMBLYAI_API_BASE}/transcript/{transcript_id}/sentences",
        headers=get_headers(api_key),
        timeout=60,
    )
    response.raise_for_status()
    return response.json()


def get_paragraphs(transcript_id: str, api_key: Optional[str] = None) -> Dict[str, Any]:
    response = requests.get(
        f"{ASSEMBLYAI_API_BASE}/transcript/{transcript_id}/paragraphs",
        headers=get_headers(api_key),
        timeout=60,
    )
    response.raise_for_status()
    return response.json()
