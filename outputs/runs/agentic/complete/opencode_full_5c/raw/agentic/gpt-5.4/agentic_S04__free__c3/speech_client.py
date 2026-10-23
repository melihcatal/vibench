from __future__ import annotations

import os
from typing import Any, Dict, Optional

import requests

from speech_models import (
    BatchTranscriptionRequest,
    TranscriptionJob,
    normalize_transcription,
)


ASSEMBLYAI_API_BASE = "https://api.assemblyai.com/v2"
ASSEMBLYAI_API_KEY_ENV = "ASSEMBLYAI_API_KEY"


class AssemblyAIBatchSpeechClient:
    def __init__(self, api_key: Optional[str] = None, timeout: int = 60) -> None:
        self.api_key = api_key or os.getenv(ASSEMBLYAI_API_KEY_ENV)
        if not self.api_key:
            raise ValueError(f"Missing {ASSEMBLYAI_API_KEY_ENV}")
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update(
            {
                "authorization": self.api_key,
                "content-type": "application/json",
            }
        )

    def submit_transcription(
        self, request: BatchTranscriptionRequest
    ) -> TranscriptionJob:
        response = self.session.post(
            f"{ASSEMBLYAI_API_BASE}/transcript",
            json=request.to_assemblyai_payload(),
            timeout=self.timeout,
        )
        response.raise_for_status()
        return normalize_transcription(response.json())

    def get_transcription(self, transcript_id: str) -> TranscriptionJob:
        response = self.session.get(
            f"{ASSEMBLYAI_API_BASE}/transcript/{transcript_id}",
            timeout=self.timeout,
        )
        response.raise_for_status()
        return normalize_transcription(response.json())

    def wait_for_completion(
        self, transcript_id: str, max_polls: int = 60, poll_interval_seconds: int = 5
    ) -> TranscriptionJob:
        import time

        for _ in range(max_polls):
            job = self.get_transcription(transcript_id)
            if job.status in {"completed", "error"}:
                return job
            time.sleep(poll_interval_seconds)
        return self.get_transcription(transcript_id)


def transcript_to_segments(job: TranscriptionJob) -> Dict[str, Any]:
    return {
        "transcript_id": job.transcript_id,
        "status": job.status,
        "text": job.text,
        "utterances": [segment.__dict__ for segment in job.utterances],
        "words": [segment.__dict__ for segment in job.words],
        "confidence": job.confidence,
    }
