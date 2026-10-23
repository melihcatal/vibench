import os
import requests
import uuid
from document_models import TranslatedText

def ocr_translate(text: str, to_language: str, from_language: str = "en", config=None) -> TranslatedText:
    if config is None:
        config = {}

    # Azure Translator Text API details
    key = config.get('translator_api_key') or os.environ.get("AZURE_TRANSLATOR_TEXT_KEY")
    endpoint = config.get('translator_endpoint') or os.environ.get("AZURE_TRANSLATOR_TEXT_ENDPOINT")
    location = config.get('translator_location') or os.environ.get("AZURE_TRANSLATOR_TEXT_LOCATION")

    if not all([key, endpoint, location]):
        raise ValueError("Azure Translator Text API key, endpoint, and location must be provided in config or environment variables.")

    path = '/translate'
    constructed_url = endpoint + path

    params = {
        'api-version': '3.0',
        'from': from_language,
        'to': [to_language]
    }

    headers = {
        'Ocp-Apim-Subscription-Key': key,
        'Ocp-Apim-Subscription-Region': location,
        'Content-type': 'application/json',
        'X-ClientTraceId': str(uuid.uuid4())
    }

    body = [{'text': text}]

    request = requests.post(constructed_url, params=params, headers=headers, json=body)
    response = request.json()

    translated_text_content = ""
    if response and isinstance(response, list) and response[0].get('translations'):
        translated_text_content = response[0]['translations'][0]['text']

    return TranslatedText(
        text=translated_text_content,
        from_language=from_language,
        to_language=to_language
    )
