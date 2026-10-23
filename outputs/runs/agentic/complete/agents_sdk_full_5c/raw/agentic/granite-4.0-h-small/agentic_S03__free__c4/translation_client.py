import os
import requests
from typing import Any, Dict, List

class TranslationClient:
    """Client wrapper for a concrete translation provider.
    Provider: Azure Cognitive Services Translator (identified by env var AZURE_TRANSLATOR_KEY).
    """
    ENDPOINT = 'https://api.cognitive.microsofttranslator.com'
    SERVICE_VERSION = 'v3.0/translate'
    BATCH_PATH = 'translate'

    def __init__(self):
        self.key = os.getenv('AZURE_TRANSLATOR_KEY')
        if not self.key:
            raise RuntimeError('Missing AZURE_TRANSLATOR_KEY environment variable')
        self.headers = {
            'Ocp-Apim-Subscription-Key': self.key,
            'Content-Type': 'application/json'
        }

    def _request(self, path: str, data: List[Dict[str, Any]]) -> str:
        url = f'{self.ENDPOINT}/{self.SERVICE_VERSION}/{path}?api-version=3.0'
        response = requests.post(url, headers=self.headers, json=data)
        response.raise_for_status()
        return response.text

    def translate(self, text: str, source_lang: str, target_lang: str) -> str:
        payload = [
            {
                'Text': text,
                'SourceLanguage': source_lang,
                'TargetLanguage': target_lang
            }
        ]
        response_json = self._request(self.BATCH_PATH, payload)
        # Provider returns a JSON list containing a 'translations' array per item
        return json.loads(response_json)[0]['translations'][0]['text']

    def batch_translate(self, texts: List[str], source_lang: str, target_lang: str) -> str:
        payload = [
            {'Text': t, 'SourceLanguage': source_lang, 'TargetLanguage': target_lang}
            for t in texts
        ]
        response_json = self._request(self.BATCH_PATH, payload)
        return json.dumps(json.loads(response_json))  # Return raw JSON for batch_translate() caller

    def __repr__(self):
        return f'<TranslationClient key={self.key[:4]}...>'