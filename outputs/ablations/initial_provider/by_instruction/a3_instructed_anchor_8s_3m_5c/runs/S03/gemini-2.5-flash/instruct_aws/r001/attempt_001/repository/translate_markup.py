import os
import requests
import uuid

from translation_models import TranslationRequest, TranslationResponse

def translate_markup_azure(request: TranslationRequest) -> TranslationResponse:
    key = os.environ.get("AZURE_TRANSLATOR_KEY")
    endpoint = os.environ.get("AZURE_TRANSLATOR_ENDPOINT", "https://api.cognitive.microsofttranslator.com")
    location = os.environ.get("AZURE_TRANSLATOR_LOCATION", "global")

    path = '/translate'
    constructed_url = endpoint + path

    params = {
        'api-version': '3.0',
        'from': request.source_language,
        'to': request.target_language,
        'textType': 'html'
    }

    headers = {
        'Ocp-Apim-Subscription-Key': key,
        'Ocp-Apim-Subscription-Region': location,
        'Content-type': 'application/json',
        'X-ClientTraceId': str(uuid.uuid4())
    }

    body = [{'text': request.text}]

    response = requests.post(constructed_url, params=params, headers=headers, json=body)
    response.raise_for_status()
    result = response.json()

    translated_text = result[0]['translations'][0]['text']
    return TranslationResponse(translated_text, request.source_language, request.target_language)
