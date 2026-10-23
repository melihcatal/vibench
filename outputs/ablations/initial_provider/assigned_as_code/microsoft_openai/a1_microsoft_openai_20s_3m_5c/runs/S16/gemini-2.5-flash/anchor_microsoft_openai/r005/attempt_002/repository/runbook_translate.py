import os
import requests
import uuid
from security_models import TranslationRequest, TranslationResponse

def runbook_translate(payload: dict, config: dict = None) -> dict:
    config = config or {}

    # Azure Translator Text API credentials and configuration
    key = os.environ.get("TRANSLATOR_TEXT_KEY") or config.get('translator_text_key')
    endpoint = os.environ.get("TRANSLATOR_TEXT_ENDPOINT") or config.get('translator_text_endpoint')
    location = os.environ.get("TRANSLATOR_TEXT_LOCATION") or config.get('translator_text_location')

    if not key or not endpoint or not location:
        raise ValueError("Azure Translator Text API key, endpoint, and location must be provided or set in environment variables.")

    path = '/translate'
    constructed_url = endpoint + path

    headers = {
        'Ocp-Apim-Subscription-Key': key,
        'Ocp-Apim-Subscription-Region': location,
        'Content-type': 'application/json',
        'X-ClientTraceId': str(uuid.uuid4())
    }

    request_payload = TranslationRequest(text=payload['text'], to_language=payload.get('to_language', 'en'))

    body = [{'text': request_payload.text}]

    params = {
        'api-version': '3.0',
        'to': request_payload.to_language
    }

    request = requests.post(constructed_url, params=params, headers=headers, json=body)
    response = request.json()

    translated_text = response[0]['translations'][0]['text']
    translation_response = TranslationResponse(translated_text=translated_text)

    return {"translation_result": translation_response.__dict__}
