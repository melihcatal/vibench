import os
import requests

class AzureSpeechClient:
    def __init__(self, region: str = None, api_key: str = None):
        self.region = region or os.environ.get("AZURE_SPEECH_REGION")
        self.api_key = api_key or os.environ.get("AZURE_SPEECH_KEY")
        if not self.region or not self.api_key:
            raise ValueError("Azure Speech region and API key must be provided or set in environment variables.")
        self.base_url = f"https://{self.region}.api.cognitive.microsoft.com/speechtotext/v3.1"

    def _get_headers(self):
        return {"Ocp-Apim-Subscription-Key": self.api_key}

    def submit_transcription(self, display_name: str, locale: str, content_urls: list, properties: dict = None):
        url = f"{self.base_url}/transcriptions"
        json_payload = {
            "displayName": display_name,
            "locale": locale,
            "contentUrls": content_urls,
            "properties": properties or {}
        }
        response = requests.post(url, headers=self._get_headers(), json=json_payload)
        response.raise_for_status()
        return response.json()

    def get_transcription(self, transcription_id: str):
        url = f"{self.base_url}/transcriptions/{transcription_id}"
        response = requests.get(url, headers=self._get_headers())
        response.raise_for_status()
        return response.json()

    def get_transcription_files(self, transcription_id: str):
        url = f"{self.base_url}/transcriptions/{transcription_id}/files"
        response = requests.get(url, headers=self._get_headers())
        response.raise_for_status()
        return response.json()
