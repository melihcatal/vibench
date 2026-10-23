import os
import requests

class AzureSpeechClient:
    def __init__(self, region: str, api_key: str = None):
        self.region = region
        self.api_key = api_key or os.environ.get("AZURE_SPEECH_KEY")
        if not self.api_key:
            raise ValueError("Azure Speech API key not provided and AZURE_SPEECH_KEY environment variable not set.")
        self.base_url = f"https://{self.region}.api.cognitive.microsoft.com/speechtotext/v3.1"

    def submit_transcription(self, display_name: str, locale: str, content_urls: list):
        headers = {'Ocp-Apim-Subscription-Key': self.api_key}
        json_payload = {
            'displayName': display_name,
            'locale': locale,
            'contentUrls': content_urls,
            'properties': {
                'wordLevelTimestampsEnabled': True,
                'diarizationEnabled': True,
            }
        }
        response = requests.post(f"{self.base_url}/transcriptions", headers=headers, json=json_payload, timeout=30)
        response.raise_for_status()
        return response.json()

    def get_transcription(self, transcription_id: str):
        headers = {'Ocp-Apim-Subscription-Key': self.api_key}
        response = requests.get(f"{self.base_url}/transcriptions/{transcription_id}", headers=headers, timeout=30)
        response.raise_for_status()
        return response.json()

    def get_transcription_files(self, transcription_id: str):
        headers = {'Ocp-Apim-Subscription-Key': self.api_key}
        response = requests.get(f"{self.base_url}/transcriptions/{transcription_id}/files", headers=headers, timeout=30)
        response.raise_for_status()
        return response.json()

    def get_file_content(self, content_url: str):
        headers = {'Ocp-Apim-Subscription-Key': self.api_key}
        response = requests.get(content_url, headers=headers, timeout=30)
        response.raise_for_status()
        return response.json()
