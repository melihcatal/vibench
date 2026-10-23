import os
import requests
from speech_models import TranscriptionConfig


class AzureSpeechClient:
    def __init__(self, region: str = None, api_key: str = None):
        self.region = region or os.environ.get('AZURE_SPEECH_REGION')
        self.api_key = api_key or os.environ.get('AZURE_SPEECH_KEY')

        if not self.region or not self.api_key:
            raise ValueError("Azure Speech region and API key must be provided or set in environment variables.")

        self.base_url = f"https://{self.region}.api.cognitive.microsoft.com/speechtotext/v3.1"

    def submit_transcription_job(self, config: TranscriptionConfig):
        headers = {
            'Ocp-Apim-Subscription-Key': self.api_key,
            'Content-Type': 'application/json'
        }
        payload = {
            'contentUrls': [config.audio_uri],
            'locale': config.language_code,
            'displayName': config.display_name,
            'properties': {
                'diarizationEnabled': config.diarization_enabled,
                'wordLevelTimestampsEnabled': config.word_level_timestamps_enabled,
                'languageIdentification': {
                    'candidateLocales': [config.language_code]
                }
            }
        }
        response = requests.post(
            f"{self.base_url}/transcriptions",
            headers=headers,
            json=payload,
            timeout=30
        )
        response.raise_for_status()
        return response.json()

    def get_transcription_job(self, job_id: str):
        headers = {
            'Ocp-Apim-Subscription-Key': self.api_key
        }
        response = requests.get(
            f"{self.base_url}/transcriptions/{job_id}",
            headers=headers,
            timeout=30
        )
        response.raise_for_status()
        return response.json()

    def get_transcription_result(self, result_url: str):
        headers = {
            'Ocp-Apim-Subscription-Key': self.api_key
        }
        response = requests.get(
            result_url,
            headers=headers,
            timeout=30
        )
        response.raise_for_status()
        return response.json()
