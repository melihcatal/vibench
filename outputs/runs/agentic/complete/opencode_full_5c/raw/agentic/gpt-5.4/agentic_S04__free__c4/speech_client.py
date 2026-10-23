from __future__ import annotations

import os
from typing import Any

import requests

from speech_models import (
    TranscriptResult,
    TranscriptionJobRequest,
    normalize_transcript_result,
)


ASSEMBLYAI_BASE_URL = "https://api.assemblyai.com/v2"
DEFAULT_TRANSCRIBER_MODEL = "best"


class AssemblyAISpeechClient:
    def __init__(self, api_key: str | None = None, timeout: float = 60.0) -> None:
        self.api_key = api_key or os.environ["ASSEMBLYAI_API_KEY"]
        self.timeout = timeout

    @property
    def headers(self) -> dict[str, str]:
        return {
            "authorization": self.api_key,
            "content-type": "application/json",
        }

    def submit_transcription(self, request: TranscriptionJobRequest) -> dict[str, Any]:
        payload = request.to_assemblyai_payload()
        payload["speech_model"] = DEFAULT_TRANSCRIBER_MODEL
        response = requests.post(
            f"{ASSEMBLYAI_BASE_URL}/transcript",
            headers=self.headers,
            json=payload,
            timeout=self.timeout,
        )
        response.raise_for_status()
        return response.json()

    def get_transcription(self, transcript_id: str) -> TranscriptResult:
        response = requests.get(
            f"{ASSEMBLYAI_BASE_URL}/transcript/{transcript_id}",
            headers=self.headers,
            timeout=self.timeout,
        )
        response.raise_for_status()
        return normalize_transcript_result(response.json())

    def get_raw_transcription(self, transcript_id: str) -> dict[str, Any]:
        response = requests.get(
            f"{ASSEMBLYAI_BASE_URL}/transcript/{transcript_id}",
            headers=self.headers,
            timeout=self.timeout,
        )
        response.raise_for_status()
        return response.json()
