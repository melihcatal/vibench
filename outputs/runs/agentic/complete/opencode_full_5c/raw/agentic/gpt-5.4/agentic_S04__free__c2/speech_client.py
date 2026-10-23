from __future__ import annotations

import os
from typing import Any

import requests

from speech_models import (
    BatchTranscriptionRequest,
    BatchTranscriptionResult,
    normalize_transcription_result,
)


ASSEMBLYAI_BASE_URL = "https://api.assemblyai.com/v2"
ASSEMBLYAI_API_KEY_ENV = "ASSEMBLYAI_API_KEY"


def get_assemblyai_api_key() -> str:
    api_key = os.getenv(ASSEMBLYAI_API_KEY_ENV)
    if not api_key:
        raise RuntimeError(
            f"Missing required environment variable: {ASSEMBLYAI_API_KEY_ENV}"
        )
    return api_key


def get_assemblyai_headers() -> dict[str, str]:
    return {
        "authorization": get_assemblyai_api_key(),
        "content-type": "application/json",
    }


def create_session() -> requests.Session:
    session = requests.Session()
    session.headers.update(get_assemblyai_headers())
    return session


def submit_batch_transcription(
    request: BatchTranscriptionRequest,
) -> BatchTranscriptionResult:
    with create_session() as session:
        response = session.post(
            f"{ASSEMBLYAI_BASE_URL}/transcript",
            json=request.to_assemblyai_payload(),
            timeout=60,
        )
        response.raise_for_status()
        return normalize_transcription_result(response.json())


def fetch_transcription(transcript_id: str) -> BatchTranscriptionResult:
    with create_session() as session:
        response = session.get(
            f"{ASSEMBLYAI_BASE_URL}/transcript/{transcript_id}", timeout=60
        )
        response.raise_for_status()
        return normalize_transcription_result(response.json())


def ensure_completed(result: BatchTranscriptionResult) -> BatchTranscriptionResult:
    if result.status == "error":
        raise RuntimeError(result.raw.get("error") or "AssemblyAI transcription failed")
    if result.status != "completed":
        raise RuntimeError(f"Transcription is not complete: {result.status}")
    return result


def transcript_payload_with_options(
    transcript_id: str, **options: Any
) -> dict[str, Any]:
    payload: dict[str, Any] = {"transcript_ids": [transcript_id]}
    payload.update({key: value for key, value in options.items() if value is not None})
    return payload
