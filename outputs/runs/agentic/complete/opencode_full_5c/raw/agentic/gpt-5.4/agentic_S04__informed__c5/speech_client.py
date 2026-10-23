from __future__ import annotations

import os
from typing import Any, Dict

import requests

from speech_models import TranscriptionJobRequest


ASSEMBLYAI_API_BASE = "https://api.assemblyai.com/v2"


def get_assemblyai_api_key() -> str:
    api_key = os.getenv("ASSEMBLYAI_API_KEY")
    if not api_key:
        raise RuntimeError("ASSEMBLYAI_API_KEY is required")
    return api_key


def build_assemblyai_headers() -> Dict[str, str]:
    return {
        "authorization": get_assemblyai_api_key(),
        "content-type": "application/json",
    }


def assemblyai_post(path: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    response = requests.post(
        f"{ASSEMBLYAI_API_BASE}{path}",
        headers=build_assemblyai_headers(),
        json=payload,
        timeout=60,
    )
    response.raise_for_status()
    return response.json()


def assemblyai_get(path: str) -> Dict[str, Any]:
    response = requests.get(
        f"{ASSEMBLYAI_API_BASE}{path}",
        headers=build_assemblyai_headers(),
        timeout=60,
    )
    response.raise_for_status()
    return response.json()


def build_batch_transcription_payload(
    request: TranscriptionJobRequest,
) -> Dict[str, Any]:
    payload: Dict[str, Any] = {
        "audio_url": request.audio_url,
        "language_code": request.language_code,
        "speaker_labels": request.speaker_labels,
        "word_boost": [],
        "punctuate": True,
        "format_text": True,
        "speech_model": "best",
    }
    if request.speakers_expected is not None:
        payload["speakers_expected"] = request.speakers_expected
    if request.word_timestamps:
        payload["word_boost"] = []
    return payload
