import os
import requests
import uuid
import json

from storage_models import StoredTextTranslateRequest, StoredTextTranslateResponse

def stored_text_translate(request: StoredTextTranslateRequest) -> StoredTextTranslateResponse:
    endpoint = os.getenv("AZURE_TRANSLATOR_ENDPOINT")
    key = os.getenv("AZURE_TRANSLATOR_KEY")
    location = os.getenv("AZURE_TRANSLATOR_LOCATION") # e.g., "global" or a specific region

    if not endpoint or not key or not location:
        raise ValueError("AZURE_TRANSLATOR_ENDPOINT, AZURE_TRANSLATOR_KEY, and AZURE_TRANSLATOR_LOCATION environment variables not set.")

    path = '/translate'
    constructed_url = endpoint + path

    headers = {
        'Ocp-Apim-Subscription-Key': key,
        'Ocp-Apim-Subscription-Region': location,
        'Content-type': 'application/json',
        'X-ClientTraceId': str(uuid.uuid4())
    }

    params = {
        'api-version': '3.0',
        'from': request.source_language,
        'to': [request.target_language]
    }

    body = [{'text': request.text}]

    response = requests.post(constructed_url, params=params, headers=headers, json=body)
    response.raise_for_status() # Raise an exception for bad status codes
    result = response.json()

    translated_text = result[0]['translations'][0]['text']
    return StoredTextTranslateResponse(translated_text=translated_text)
