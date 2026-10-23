import os
import requests


class AzureSpeechClient:
    def __init__(self, region: str, api_key: str):
        self.region = region
        self.api_key = api_key
        self.base_url = f"https://{self.region}.api.cognitive.microsoft.com/speechtotext/v3.2" # Updated API version to 3.2 based on documentation
        self.headers = {
            'Ocp-Apim-Subscription-Key': self.api_key,
            'Content-Type': 'application/json'
        }

    def _make_request(self, method: str, endpoint: str, json_payload=None, params=None):
        url = f"{self.base_url}/{endpoint}"
        response = requests.request(method, url, headers=self.headers, json=json_payload, params=params, timeout=30)
        response.raise_for_status()
        return response.json()

    def submit_transcription_job(self, display_name: str, locale: str, content_urls: list, diarization_enabled: bool = False, word_level_timestamps_enabled: bool = False):
        properties = {}
        if diarization_enabled:
            properties['diarizationEnabled'] = True
        if word_level_timestamps_enabled:
            properties['wordLevelTimestampsEnabled'] = True

        payload = {
            'displayName': display_name,
            'locale': locale,
            'contentUrls': content_urls,
            'properties': properties
        }
        return self._make_request('POST', 'transcriptions', json_payload=payload)

    def get_transcription_job(self, job_id: str):
        return self._make_request('GET', f'transcriptions/{job_id}')

    def get_transcription_results(self, job_id: str):
        return self._make_request('GET', f'transcriptions/{job_id}/files')
