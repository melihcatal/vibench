from __future__ import annotations

import os
from typing import Any, Dict, Optional

import requests

from speech_models import (
    BatchTranscriptionRequest,
    BatchTranscriptionResult,
    normalize_transcription_result,
)


ASSEMBLYAI_API_BASE = "https://api.assemblyai.com/v2"
ASSEMBLYAI_DEFAULT_MODEL = "best"


class AssemblyAIClient:
    def __init__(
        self,
        api_key: Optional[str] = None,
        api_base: str = ASSEMBLYAI_API_BASE,
        timeout: int = 60,
    ) -> None:
        self.api_key = api_key or os.environ["ASSEMBLYAI_API_KEY"]
        self.api_base = api_base.rstrip("/")
        self.timeout = timeout

    @property
    def headers(self) -> Dict[str, str]:
        return {
            "authorization": self.api_key,
            "content-type": "application/json",
        }

    def submit_transcription(
        self, request: BatchTranscriptionRequest
    ) -> BatchTranscriptionResult:
        payload = request.to_assemblyai_payload()
        payload.setdefault("speech_model", ASSEMBLYAI_DEFAULT_MODEL)
        response = requests.post(
            f"{self.api_base}/transcript",
            headers=self.headers,
            json=payload,
            timeout=self.timeout,
        )
        response.raise_for_status()
        return normalize_transcription_result(response.json())

    def get_transcription(self, transcript_id: str) -> BatchTranscriptionResult:
        response = requests.get(
            f"{self.api_base}/transcript/{transcript_id}",
            headers=self.headers,
            timeout=self.timeout,
        )
        response.raise_for_status()
        return normalize_transcription_result(response.json())

    def poll_until_complete(
        self, transcript_id: str, max_attempts: int = 60, interval_seconds: float = 5.0
    ) -> BatchTranscriptionResult:
        import time

        last_result: Optional[BatchTranscriptionResult] = None
        for _ in range(max_attempts):
            last_result = self.get_transcription(transcript_id)
            if last_result.status in {"completed", "error"}:
                return last_result
            time.sleep(interval_seconds)
        if last_result is None:
            raise RuntimeError("AssemblyAI transcription polling returned no result")
        return last_result


def build_transcription_request(
    audio_url: str,
    language_code: Optional[str] = None,
    speaker_labels: bool = False,
    speaker_count: Optional[int] = None,
    webhook_url: Optional[str] = None,
) -> BatchTranscriptionRequest:
    return BatchTranscriptionRequest(
        audio_url=audio_url,
        language_code=language_code,
        speaker_labels=speaker_labels,
        speaker_count=speaker_count,
        webhook_url=webhook_url,
    )
