import os
import requests
from typing import Dict, Any, List

class AzureTranslatorClient:
    def __init__(self, api_key: str, region: str, endpoint: str = "https://api.cognitive.microsofttranslator.com"):
        self.api_key = api_key
        self.region = region
        self.endpoint = endpoint
        self.headers = {
            'Ocp-Apim-Subscription-Key': self.api_key,
            'Ocp-Apim-Subscription-Region': self.region,
            'Content-type': 'application/json'
        }
        self.params = {
            'api-version': '3.0'
        }

    def translate(self, text_elements: List[Dict[str, str]], source_language: str, target_language: str, text_type: str = "plain") -> List[Dict[str, Any]]:
        params = self.params.copy()
        params['from'] = source_language
        params['to'] = target_language
        if text_type == "html":
            params['textType'] = "html"

        response = requests.post(f'{self.endpoint}/translate',
            headers=self.headers,
            params=params,
            json=text_elements,
            timeout=30)
        response.raise_for_status()
        return response.json()

def get_azure_translator_client() -> AzureTranslatorClient:
    api_key = os.environ.get("AZURE_TRANSLATOR_API_KEY")
    region = os.environ.get("AZURE_TRANSLATOR_REGION")
    if not api_key or not region:
        raise ValueError("AZURE_TRANSLATOR_API_KEY and AZURE_TRANSLATOR_REGION environment variables must be set.")
    return AzureTranslatorClient(api_key=api_key, region=region)
