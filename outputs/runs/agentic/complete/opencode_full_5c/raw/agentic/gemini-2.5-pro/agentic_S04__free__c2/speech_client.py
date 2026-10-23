import os
import requests


class AssemblyAIClient:
    def __init__(self):
        self.api_key = os.environ.get("ASSEMBLYAI_API_KEY")
        self.base_url = "https://api.assemblyai.com/v2"

    def get_headers(self):
        return {"authorization": self.api_key}

    def submit_transcription(self, audio_url: str, options: dict = None):
        if options is None:
            options = {}
        payload = {"audio_url": audio_url, **options}
        response = requests.post(
            f"{self.base_url}/transcript", json=payload, headers=self.get_headers()
        )
        response.raise_for_status()
        return response.json()

    def get_transcription(self, transcript_id: str):
        response = requests.get(
            f"{self.base_url}/transcript/{transcript_id}", headers=self.get_headers()
        )
        response.raise_for_status()
        return response.json()
