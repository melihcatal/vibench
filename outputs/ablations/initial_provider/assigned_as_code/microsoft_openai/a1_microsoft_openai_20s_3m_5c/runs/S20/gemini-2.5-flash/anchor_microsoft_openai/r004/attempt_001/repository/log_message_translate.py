import os
import requests
import uuid
import json
from typing import Dict, Any
from observability_models import TranslateRequest, TranslateResponse

def translate_log_message(request: TranslateRequest, config: Dict[str, Any] = None) -> TranslateResponse:
    config = config or {}

    translator_endpoint = config.get('AZURE_TRANSLATOR_ENDPOINT', os.environ.get('AZURE_TRANSLATOR_ENDPOINT'))
    translator_key = config.get('AZURE_TRANSLATOR_KEY', os.environ.get('AZURE_TRANSLATOR_KEY'))
    translator_region = config.get('AZURE_TRANSLATOR_REGION', os.environ.get('AZURE_TRANSLATOR_REGION'))

    if not all([translator_endpoint, translator_key, translator_region]):
        raise ValueError("Azure Translator endpoint, key, or region not configured.")

    path = '/translate'
    constructed_url = translator_endpoint + path

    headers = {
        'Ocp-Apim-Subscription-Key': translator_key,
        'Ocp-Apim-Subscription-Region': translator_region,
        'Content-type': 'application/json',
        'X-ClientTraceId': str(uuid.uuid4())
    }

    params = {
        'api-version': '3.0',
        'to': request.target_locale
    }

    body = [{'text': request.text}]

    response = requests.post(constructed_url, params=params, headers=headers, json=body)
    response.raise_for_status() # Raise an exception for HTTP errors

    translation_result = response.json()

    if translation_result and len(translation_result) > 0 and 'translations' in translation_result[0]:
        translated_text = translation_result[0]['translations'][0]['text']
    else:
        translated_text = request.text # Return original if translation fails or is empty

    return TranslateResponse(translated_text=translated_text)
