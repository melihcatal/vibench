import os
import requests
from speech_models import TranscriptionConfig

class AzureSpeechClient:
    def __init__(self, config: TranscriptionConfig):
        self.config = config
        self.api_key = config.api_key or os.environ.get('AZURE_SPEECH_KEY')
        if not self.api_key:
            raise ValueError("Azure Speech API key not found. Please set AZURE_SPEECH_KEY environment variable or pass it in config.")
        self.region = config.region
        self.base_url = f"https://{{self.region}}.api.cognitive.microsoft.com/speechtotext/v3.2"

    def _get_headers(self):
        return {
            'Ocp-Apim-Subscription-Key': self.api_key,
            'Content-Type': 'application/json'
        }

    def submit_transcription_job(self, display_name: str, locale: str, content_urls: list, properties: dict = None):
        url = f"{self.base_url}/transcriptions"
        body = {
            'displayName': display_name,
            'locale': locale,
            'contentUrls': content_urls,
            'properties': properties or {}
        }
        response = requests.post(url, headers=self._get_headers(), json=body)
        response.raise_for_status()
        return response.json()

    def get_transcription_job(self, job_id: str):
        url = f"{self.base_url}/transcriptions/{job_id}"
        response = requests.get(url, headers=self._get_headers())
        response.raise_for_status()
        return response.json()

    def get_transcription_result(self, result_uri: str):
        response = requests.get(result_uri, headers=self._get_headers())
        response.raise_for_status()
        return response.json()
