import os
import requests
from speech_models import TranscriptionConfig

class AzureSpeechClient:
    def __init__(self, config: TranscriptionConfig):
        self.region = config.region
        self.api_key = config.api_key
        self.base_url = f"https://{self.region}.api.cognitive.microsoft.com/speechtotext/v3.1"

    def _headers(self):
        return {'Ocp-Apim-Subscription-Key': self.api_key}

    def submit_transcription_job(self, display_name: str, locale: str, content_urls: list, properties: dict = None):
        properties = properties or {}
        payload = {
            'displayName': display_name,
            'locale': locale,
            'contentUrls': content_urls,
            'properties': properties
        }
        url = f"{self.base_url}/transcriptions"
        response = requests.post(url, headers=self._headers(), json=payload, timeout=30)
        response.raise_for_status()
        return response.json()

    def get_transcription_status(self, job_id: str):
        url = f"{self.base_url}/transcriptions/{job_id}"
        response = requests.get(url, headers=self._headers(), timeout=30)
        response.raise_for_status()
        return response.json()

    def get_transcription_result(self, job_id: str, result_url: str):
        headers = self._headers()
        headers['Accept'] = 'application/json'
        response = requests.get(result_url, headers=headers, timeout=30)
        response.raise_for_status()
        return response.json()
