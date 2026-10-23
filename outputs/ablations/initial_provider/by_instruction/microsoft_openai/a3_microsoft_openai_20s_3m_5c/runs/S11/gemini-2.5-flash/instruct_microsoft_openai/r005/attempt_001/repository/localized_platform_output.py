import os
import requests
import uuid

def translate_text(text: str, target_language: str, source_language: str = "en") -> dict:
    key = os.environ.get("AZURE_TRANSLATOR_KEY")
    endpoint = os.environ.get("AZURE_TRANSLATOR_ENDPOINT")
    location = os.environ.get("AZURE_TRANSLATOR_REGION")

    if not key or not endpoint or not location:
        raise ValueError("Azure Translator key, endpoint, and region must be set in environment variables.")

    path = '/translate'
    constructed_url = endpoint + path

    params = {
        'api-version': '3.0',
        'from': source_language,
        'to': [target_language]
    }

    headers = {
        'Ocp-Apim-Subscription-Key': key,
        'Ocp-Apim-Subscription-Region': location,
        'Content-type': 'application/json',
        'X-ClientTraceId': str(uuid.uuid4())
    }

    body = [{
        'text': text
    }]

    request = requests.post(constructed_url, params=params, headers=headers, json=body)
    response = request.json()

    if response and isinstance(response, list) and 'translations' in response[0]:
        return response[0]['translations'][0]
    else:
        raise Exception(f"Translation failed: {response}")
