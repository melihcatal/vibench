import os
import requests
from typing import Any, Dict

BASE_URL = os.getenv('BATCH_SPEECH_ENDPOINT')
API_KEY = os.getenv('BATCH_SPEECH_API_KEY')
PROVIDER = 'azure_speech'  # identifier used in other modules


class SpeechClient:
    """Thin wrapper around the batch speech-to-text service API."""
    def __init__(self, base_url: str, api_key: str, provider: str):
        self.base_url = base_url.rstrip('/')
        self.api_key = api_key
        self.provider = provider
        self.session = requests.Session()
        self.session.headers.update({'Ocp-Apim-Subscription-Key': self.api_key})

    def _request(self, method: str, path: str, json: Any = None, params: Any = None):
        url = f'{self.base_url}{path}'
        response = self.session.request(method, url, json=json, params=params)
        response.raise_for_status()
        return response.json()

    def post(self, path: str, json: Any = None, params: Any = None):
        return self._request('POST', path, json=json, params=params)

    def get(self, path: str, params: Any = None):
        return self._request('GET', path, params=params)

    def put(self, path: str, json: Any = None):
        return self._request('PUT', path, json=json)

    def delete(self, path: str):
        return self._request('DELETE', path)
