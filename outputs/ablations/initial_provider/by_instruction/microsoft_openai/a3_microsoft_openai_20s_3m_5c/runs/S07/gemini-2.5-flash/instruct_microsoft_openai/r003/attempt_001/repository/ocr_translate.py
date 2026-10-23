import os
import requests
import uuid
import json

def translate_text(text: str, target_language: str = "en") -> str:
    # Azure AI Translator Text API endpoint and key
    endpoint = os.environ.get("TRANSLATOR_ENDPOINT")
    key = os.environ.get("TRANSLATOR_KEY")
    region = os.environ.get("TRANSLATOR_REGION")

    if not endpoint or not key or not region:
        raise ValueError("TRANSLATOR_ENDPOINT, TRANSLATOR_KEY, and TRANSLATOR_REGION environment variables must be set.")

    path = '/translate'
    constructed_url = endpoint + path

    headers = {
        'Ocp-Apim-Subscription-Key': key,
        'Ocp-Apim-Subscription-Region': region,
        'Content-type': 'application/json',
        'X-ClientTraceId': str(uuid.uuid4())
    }

    params = {
        'api-version': '3.0',
        'to': target_language
    }

    body = [{
        'text': text
    }]

    request = requests.post(constructed_url, params=params, headers=headers, json=body)
    response = request.json()

    translated_text = ""
    if response and isinstance(response, list) and len(response) > 0 and "translations" in response[0] and len(response[0]["translations"]) > 0:
        translated_text = response[0]["translations"][0]["text"]
    
    return translated_text
