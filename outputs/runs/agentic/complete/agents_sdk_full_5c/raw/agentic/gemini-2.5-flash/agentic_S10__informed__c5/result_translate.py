import os
import requests
import uuid
from typing import Dict, Any

def translate_text(text: str, to_language: str = "es", from_language: str = "en") -> Dict[str, Any]:
    """Translate generated model output using Azure AI Translator."""
    endpoint = os.getenv("AZURE_TRANSLATOR_ENDPOINT")
    key = os.getenv("AZURE_TRANSLATOR_KEY")
    region = os.getenv("AZURE_TRANSLATOR_REGION")

    if not endpoint or not key or not region:
        raise ValueError("AZURE_TRANSLATOR_ENDPOINT, AZURE_TRANSLATOR_KEY, and AZURE_TRANSLATOR_REGION environment variables must be set.")

    path = '/translate'
    constructed_url = endpoint + path

    params = {
        'api-version': '3.0',
        'from': from_language,
        'to': [to_language]
    }

    headers = {
        'Ocp-Apim-Subscription-Key': key,
        'Ocp-Apim-Subscription-Region': region,
        'Content-type': 'application/json',
        'X-ClientTraceId': str(uuid.uuid4())
    }

    body = [{'text': text}]

    try:
        request = requests.post(constructed_url, params=params, headers=headers, json=body)
        request.raise_for_status()
        return request.json()
    except requests.exceptions.RequestException as e:
        print(f"Error translating text: {e}")
        raise
