import os
import requests

ASSEMBLYAI_API_KEY = os.getenv("ASSEMBLYAI_API_KEY")
API_BASE_URL = "https://api.assemblyai.com/v2"


def get_assemblyai_client():
    if not ASSEMBLYAI_API_KEY:
        raise ValueError("ASSEMBLYAI_API_KEY environment variable not set.")

    headers = {"authorization": ASSEMBLYAI_API_KEY}

    def post(endpoint, json_data):
        response = requests.post(
            f"{API_BASE_URL}{endpoint}", headers=headers, json=json_data
        )
        response.raise_for_status()
        return response.json()

    def get(endpoint):
        response = requests.get(f"{API_BASE_URL}{endpoint}", headers=headers)
        response.raise_for_status()
        return response.json()

    class AssemblyAIClient:
        def submit_transcription(self, audio_url: str, **kwargs):
            payload = {"audio_url": audio_url, **kwargs}
            return post("/transcript", payload)

        def get_transcription(self, transcript_id: str):
            return get(f"/transcript/{transcript_id}")

    return AssemblyAIClient()
