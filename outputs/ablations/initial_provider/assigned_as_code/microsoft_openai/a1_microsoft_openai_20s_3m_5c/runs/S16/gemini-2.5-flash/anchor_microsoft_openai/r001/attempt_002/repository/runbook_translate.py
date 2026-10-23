import os
import requests
from typing import List
from security_models import TranslatedText

def translate_runbook_notes(text_to_translate: str, target_language: str, azure_translator_endpoint: str = None, azure_translator_key: str = None, azure_translator_region: str = None) -> TranslatedText:
    if azure_translator_endpoint is None:
        azure_translator_endpoint = os.environ.get("AZURE_TRANSLATOR_ENDPOINT")
    if azure_translator_key is None:
        azure_translator_key = os.environ.get("AZURE_TRANSLATOR_API_KEY")
    if azure_translator_region is None:
        azure_translator_region = os.environ.get("AZURE_TRANSLATOR_REGION")

    if not azure_translator_endpoint or not azure_translator_key or not azure_translator_region:
        raise ValueError("Azure Translator endpoint, API key, and region must be provided or set in environment variables.")

    path = '/translate'
    constructed_url = azure_translator_endpoint + path

    headers = {
        'Ocp-Apim-Subscription-Key': azure_translator_key,
        'Ocp-Apim-Subscription-Region': azure_translator_region,
        'Content-type': 'application/json',
        'X-ClientTraceId': str(os.urandom(16))
    }

    params = {
        'api-version': '3.0',
        'to': target_language
    }

    body = [{'text': text_to_translate}]

    request = requests.post(constructed_url, params=params, headers=headers, json=body)
    response = request.json()

    translated_text = response[0]['translations'][0]['text']

    return TranslatedText(
        original_text=text_to_translate,
        translated_text=translated_text,
        target_language=target_language
    )
