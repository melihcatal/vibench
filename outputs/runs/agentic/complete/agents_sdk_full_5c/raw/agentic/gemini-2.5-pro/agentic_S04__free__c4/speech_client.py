import os
import requests
from typing import Optional

from speech_models import TranscriptionResponse


class AssemblyAIClient:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("ASSEMBLYAI_API_KEY")
        if not self.api_key:
            raise ValueError("AssemblyAI API key is required.")
        self.base_url = "https://api.assemblyai.com/v2"

    def _get_headers(self):
        return {
            "authorization": self.api_key,
            "content-type": "application/json",
        }

    def submit_transcription(self, audio_url: str, **kwargs) -> TranscriptionResponse:
        """Submits a new transcription job."""
        payload = {"audio_url": audio_url, **kwargs}
        response = requests.post(
            f"{self.base_url}/transcript", json=payload, headers=self._get_headers()
        )
        response.raise_for_status()
        return TranscriptionResponse(**response.json())

    def get_transcription(self, transcript_id: str) -> TranscriptionResponse:
        """Gets the status and result of a transcription job."""
        response = requests.get(
            f"{self.base_url}/transcript/{transcript_id}", headers=self._get_headers()
        )
        response.raise_for_status()
        return TranscriptionResponse(**response.json())
