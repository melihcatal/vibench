import os
import requests
from typing import Dict, Any, List

class AzureTranslationClient:
    def __init__(self, api_key: str, region: str):
        self.api_key = api_key
        self.region = region
        self.endpoint = "https://api.cognitive.microsofttranslator.com"

    def _get_headers(self) -> Dict[str, str]:
        return {
            'Ocp-Apim-Subscription-Key': self.api_key,
            'Ocp-Apim-Subscription-Region': self.region,
            'Content-type': 'application/json'
        }

    def translate(self, texts: List[Dict[str, str]], from_lang: str, to_lang: str, text_type: str = 'plain') -> List[Dict[str, Any]]:
        path = '/translate'
        constructed_url = self.endpoint + path

        params = {
            'api-version': '3.0',
            'from': from_lang,
            'to': to_lang,
            'textType': text_type # 'plain' or 'html'
        }

        response = requests.post(constructed_url, headers=self._get_headers(), params=params, json=texts, timeout=30)
        response.raise_for_status()
        return response.json()

def get_azure_translation_client(config: Dict[str, str]) -> AzureTranslationClient:
    api_key = config.get('AZURE_TRANSLATOR_API_KEY') or os.environ.get('AZURE_TRANSLATOR_API_KEY')
    region = config.get('AZURE_TRANSLATOR_REGION') or os.environ.get('AZURE_TRANSLATOR_REGION')

    if not api_key or not region:
        raise ValueError("Azure Translator API key and region must be provided in config or environment variables.")

    return AzureTranslationClient(api_key, region)
