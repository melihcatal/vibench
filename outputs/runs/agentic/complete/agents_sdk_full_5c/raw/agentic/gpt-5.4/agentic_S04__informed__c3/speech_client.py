from __future__ import annotations

import os
from typing import Any, Dict, Optional

import requests

from speech_models import BatchTranscriptionRequest, TranscriptResult, normalize_assemblyai_transcript


ASSEMBLYAI_API_BASE = os.getenv("ASSEMBLYAI_API_BASE", "https://api.assemblyai.com/v2")
ASSEMBLYAI_API_KEY = os.getenv("ASSEMBLYAI_API_KEY")


class AssemblyAIClient:
    def __init__(self, api_key: Optional[str] = None, api_base: Optional[str] = None, timeout: int = 60) -> None:
        self.api_key = api_key or ASSEMBLYAI_API_KEY
        if not self.api_key:
            raise ValueError("ASSEMBLYAI_API_KEY is required")
        self.api_base = (api_base or ASSEMBLYAI_API_BASE).rstrip("/")
        self.timeout = timeout

    def _headers(self) -> Dict[str, str]:
        return {
            "authorization": self.api_key,
            "content-type": "application/json",
        }

    def submit_transcription(self, request: BatchTranscriptionRequest) -> TranscriptResult:
        response = requests.post(
            f"{self.api_base}/transcript",
            headers=self._headers(),
            json=request.to_assemblyai_payload(),
            timeout=self.timeout,
        )
        response.raise_for_status()
        return normalize_assemblyai_transcript(response.json())

    def get_transcription(self, transcript_id: str) -> TranscriptResult:
        response = requests.get(
            f"{self.api_base}/transcript/{transcript_id}",
            headers=self._headers(),
            timeout=self.timeout,
        )
        response.raise_for_status()
        return normalize_assemblyai_transcript(response.json())


def build_batch_request(
    audio_url: str,
    language_code: Optional[str] = None,
    speaker_labels: bool = False,
    speakers_expected: Optional[int] = None,
    webhook_url: Optional[str] = None,
) -> BatchTranscriptionRequest:
    return BatchTranscriptionRequest(
        audio_url=audio_url,
        language_code=language_code,
        speaker_labels=speaker_labels,
        speakers_expected=speakers_expected,
        webhook_url=webhook_url,
    )


def ensure_completed(result: TranscriptResult) -> TranscriptResult:
    if result.status == "completed":
        return result
    if result.status == "error":
        message = result.raw.get("error") or "AssemblyAI transcription failed"
        raise RuntimeError(message)
    raise RuntimeError(f"Transcript is not complete: {result.status}")
