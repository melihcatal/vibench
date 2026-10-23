from __future__ import annotations

import os
from typing import Any, Dict, Optional

import requests

from speech_models import TranscriptionSubmitRequest


ASSEMBLYAI_BASE_URL = "https://api.assemblyai.com/v2"


class AssemblyAISpeechClient:
    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: str = ASSEMBLYAI_BASE_URL,
        timeout: int = 60,
    ):
        self.api_key = api_key or os.environ["ASSEMBLYAI_API_KEY"]
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

    @property
    def headers(self) -> Dict[str, str]:
        return {
            "authorization": self.api_key,
            "content-type": "application/json",
        }

    def submit_transcript(self, request: TranscriptionSubmitRequest) -> Dict[str, Any]:
        payload: Dict[str, Any] = {
            "audio_url": request.audio_url,
            "speaker_labels": request.speaker_labels,
            "word_boost": [],
        }
        if request.language_code:
            payload["language_code"] = request.language_code
        if request.speakers_expected is not None:
            payload["speakers_expected"] = request.speakers_expected
        if request.word_timestamps:
            payload["format_text"] = True
        response = requests.post(
            f"{self.base_url}/transcript",
            headers=self.headers,
            json=payload,
            timeout=self.timeout,
        )
        response.raise_for_status()
        return response.json()

    def get_transcript(self, transcript_id: str) -> Dict[str, Any]:
        response = requests.get(
            f"{self.base_url}/transcript/{transcript_id}",
            headers=self.headers,
            timeout=self.timeout,
        )
        response.raise_for_status()
        return response.json()
