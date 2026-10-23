import os
import requests
import uuid
import json

from storage_models import StoredTextTranslateRequest, StoredTextTranslateResponse

def stored_text_translate(request: StoredTextTranslateRequest) -> StoredTextTranslateResponse:
    key = os.getenv("AZURE_TRANSLATOR_TEXT_SUBSCRIPTION_KEY")
    endpoint = os.getenv("AZURE_TRANSLATOR_TEXT_ENDPOINT")
    location = os.getenv("AZURE_TRANSLATOR_TEXT_LOCATION")

    if not key or not endpoint or not location:
        raise ValueError("AZURE_TRANSLATOR_TEXT_SUBSCRIPTION_KEY, AZURE_TRANSLATOR_TEXT_ENDPOINT, and AZURE_TRANSLATOR_TEXT_LOCATION environment variables must be set.")

    path = '/translate'
    constructed_url = endpoint + path

    params = {
        'api-version': '3.0',
        'to': request.target_language
    }
    if request.source_language:
        params['from'] = request.source_language

    headers = {
        'Ocp-Apim-Subscription-Key': key,
        'Ocp-Apim-Subscription-Region': location,
        'Content-type': 'application/json',
        'X-ClientTraceId': str(uuid.uuid4())
    }

    body = [{
        'text': request.text_content
    }]

    response = requests.post(constructed_url, params=params, headers=headers, json=body)
    response.raise_for_status()
    response_json = response.json()

    translated_text = response_json[0]['translations'][0]['text']
    source_language = response_json[0]['detectedLanguage']['language'] if 'detectedLanguage' in response_json[0] else None

    return StoredTextTranslateResponse(translated_text=translated_text, source_language=source_language)
