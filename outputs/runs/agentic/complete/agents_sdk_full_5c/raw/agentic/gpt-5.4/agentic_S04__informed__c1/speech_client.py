from __future__ import annotations

import os
from typing import Any, Dict, Optional

import requests

from speech_models import SpeechJobRequest


ASSEMBLYAI_BASE_URL = "https://api.assemblyai.com/v2"


class AssemblyAISpeechClient:
    def __init__(self, api_key: Optional[str] = None, timeout: int = 60) -> None:
        self.api_key = api_key or os.environ.get("ASSEMBLYAI_API_KEY")
        if not self.api_key:
            raise ValueError("ASSEMBLYAI_API_KEY is required")
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update(
            {
                "authorization": self.api_key,
                "content-type": "application/json",
            }
        )

    def submit_transcription(self, request: SpeechJobRequest, extra: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        payload = request.to_assemblyai_payload()
        if extra:
            payload.update(extra)
        response = self.session.post(
            f"{ASSEMBLYAI_BASE_URL}/transcript",
            json=payload,
            timeout=self.timeout,
        )
        response.raise_for_status()
        return response.json()

    def get_transcription(self, transcript_id: str) -> Dict[str, Any]:
        response = self.session.get(
            f"{ASSEMBLYAI_BASE_URL}/transcript/{transcript_id}",
            timeout=self.timeout,
        )
        response.raise_for_status()
        return response.json()
