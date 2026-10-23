import os
import requests
import uuid
import json

AZURE_TRANSLATOR_TEXT_ENDPOINT = os.environ.get("AZURE_TRANSLATOR_TEXT_ENDPOINT")
AZURE_TRANSLATOR_TEXT_KEY = os.environ.get("AZURE_TRANSLATOR_TEXT_KEY")
AZURE_TRANSLATOR_TEXT_REGION = os.environ.get("AZURE_TRANSLATOR_TEXT_REGION", "global")

def translate_text(text: str, target_language: str = "es", source_language: str = "en") -> dict:
    if not AZURE_TRANSLATOR_TEXT_ENDPOINT or not AZURE_TRANSLATOR_TEXT_KEY:
        raise ValueError("AZURE_TRANSLATOR_TEXT_ENDPOINT and AZURE_TRANSLATOR_TEXT_KEY must be set in environment variables")

    path = '/translate'
    constructed_url = AZURE_TRANSLATOR_TEXT_ENDPOINT + path

    params = {
        'api-version': '3.0',
        'from': source_language,
        'to': [target_language]
    }

    headers = {
        'Ocp-Apim-Subscription-Key': AZURE_TRANSLATOR_TEXT_KEY,
        'Ocp-Apim-Subscription-Region': AZURE_TRANSLATOR_TEXT_REGION,
        'Content-type': 'application/json',
        'X-ClientTraceId': str(uuid.uuid4())
    }

    body = [{
        'text': text
    }]

    request = requests.post(constructed_url, params=params, headers=headers, json=body)
    response = request.json()
    return response[0]['translations'][0]['text']
