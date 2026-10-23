from __future__ import annotations

import os
from typing import Optional

import requests

from speech_models import TranscriptResult

ASSEMBLYAI_TRANSCRIPT_URL = "https://api.assemblyai.com/v2/transcript"


def transcribe_qa_sample(audio_bytes: bytes, audio_content_type: str = "audio/mpeg") -> TranscriptResult:
    api_key = os.getenv("ASSEMBLYAI_API_KEY")
    if not api_key:
        raise ValueError("ASSEMBLYAI_API_KEY is required")

    upload_response = requests.post(
        "https://api.assemblyai.com/v2/upload",
        headers={"authorization": api_key, "content-type": audio_content_type},
        data=audio_bytes,
        timeout=120,
    )
    upload_response.raise_for_status()
    audio_url = upload_response.json()["upload_url"]

    transcript_response = requests.post(
        ASSEMBLYAI_TRANSCRIPT_URL,
        headers={"authorization": api_key, "content-type": "application/json"},
        json={"audio_url": audio_url},
        timeout=60,
    )
    transcript_response.raise_for_status()
    transcript_id = transcript_response.json()["id"]

    polling_url = f"{ASSEMBLYAI_TRANSCRIPT_URL}/{transcript_id}"
    while True:
        status_response = requests.get(
            polling_url,
            headers={"authorization": api_key},
            timeout=60,
        )
        status_response.raise_for_status()
        payload = status_response.json()
        status = payload["status"]
        if status == "completed":
            return TranscriptResult(
                provider="assemblyai",
                transcript=payload.get("text", ""),
                confidence=payload.get("confidence"),
            )
        if status == "error":
            raise RuntimeError(payload.get("error", "AssemblyAI transcription failed"))
