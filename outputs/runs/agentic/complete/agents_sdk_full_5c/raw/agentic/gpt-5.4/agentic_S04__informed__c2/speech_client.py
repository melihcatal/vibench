from __future__ import annotations

import os
from typing import Optional

import requests

ASSEMBLYAI_API_URL = "https://api.assemblyai.com/v2"
DEFAULT_TRANSCRIBER_MODEL = "best"


class AssemblyAIClient:
    def __init__(self, api_key: Optional[str] = None, api_url: str = ASSEMBLYAI_API_URL) -> None:
        self.api_key = api_key or os.environ["ASSEMBLYAI_API_KEY"]
        self.api_url = api_url.rstrip("/")
        self.session = requests.Session()
        self.session.headers.update({
            "authorization": self.api_key,
            "content-type": "application/json",
        })

    def upload_audio(self, file_path: str) -> str:
        with open(file_path, "rb") as handle:
            response = self.session.post(
                f"{self.api_url}/upload",
                data=handle,
                headers={"authorization": self.api_key},
                timeout=300,
            )
        response.raise_for_status()
        return response.json()["upload_url"]

    def submit_transcript(self, payload: dict) -> dict:
        enriched = dict(payload)
        enriched.setdefault("speech_model", DEFAULT_TRANSCRIBER_MODEL)
        response = self.session.post(f"{self.api_url}/transcript", json=enriched, timeout=60)
        response.raise_for_status()
        return response.json()

    def get_transcript(self, transcript_id: str) -> dict:
        response = self.session.get(f"{self.api_url}/transcript/{transcript_id}", timeout=60)
        response.raise_for_status()
        return response.json()


def build_speech_client() -> AssemblyAIClient:
    return AssemblyAIClient()
