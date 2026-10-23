import os
import requests
from typing import Dict, Any


class SpeechClient:
    def __init__(self):
        self.api_key = os.getenv("ASSEMBLYAI_API_KEY")
        if not self.api_key:
            raise ValueError("ASSEMBLYAI_API_KEY environment variable not set")
        self.base_url = "https://api.assemblyai.com/v2"
        self.headers = {
            "authorization": self.api_key,
            "content-type": "application/json",
        }

    def submit_job(
        self, audio_url: str, params: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        payload = {"audio_url": audio_url}
        if params:
            payload.update(params)

        response = requests.post(
            f"{self.base_url}/transcript", json=payload, headers=self.headers
        )
        response.raise_for_status()
        return response.json()

    def get_job(self, job_id: str) -> Dict[str, Any]:
        response = requests.get(
            f"{self.base_url}/transcript/{job_id}", headers=self.headers
        )
        response.raise_for_status()
        return response.json()
