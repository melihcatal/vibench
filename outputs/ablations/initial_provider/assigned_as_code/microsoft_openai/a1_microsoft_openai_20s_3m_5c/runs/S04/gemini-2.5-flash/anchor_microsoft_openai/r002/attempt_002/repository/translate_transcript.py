import os
import requests
from typing import List, Dict, Any

def translate_transcript(text_segments: List[str], target_language: str, config=None) -> List[Dict[str, Any]]:
    config = config or {}
    api_key = config.get('azure_translator_key') or os.environ.get('AZURE_TRANSLATOR_KEY')
    endpoint = config.get('azure_translator_endpoint') or os.environ.get('AZURE_TRANSLATOR_ENDPOINT')
    region = config.get('azure_translator_region') or os.environ.get('AZURE_TRANSLATOR_REGION')

    if not api_key or not endpoint or not region:
        raise ValueError("Azure Translator API key, endpoint, and region must be provided or set as environment variables.")

    path = '/translate'
    constructed_url = endpoint + path

    headers = {
        'Ocp-Apim-Subscription-Key': api_key,
        'Ocp-Apim-Subscription-Region': region,
        'Content-type': 'application/json'
    }

    params = {
        'api-version': '3.0',
        'to': target_language
    }

    body = [{'text': segment} for segment in text_segments]

    response = requests.post(constructed_url, params=params, headers=headers, json=body, timeout=30)
    response.raise_for_status()
    return response.json()
