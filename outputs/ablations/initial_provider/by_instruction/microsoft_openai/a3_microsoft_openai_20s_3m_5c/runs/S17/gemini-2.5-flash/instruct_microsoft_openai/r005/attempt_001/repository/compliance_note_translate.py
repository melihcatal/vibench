import requests
import os
import uuid

def translate_note(text_to_translate: str, target_language: str, azure_translator_endpoint: str, azure_translator_key: str, azure_translator_region: str) -> str:
    """
    Translates encryption or compliance notes using Azure AI Translator.
    """
    path = '/translate'
    constructed_url = azure_translator_endpoint + path

    headers = {
        'Ocp-Apim-Subscription-Key': azure_translator_key,
        'Ocp-Apim-Subscription-Region': azure_translator_region,
        'Content-type': 'application/json',
        'X-ClientTraceId': str(uuid.uuid4())
    }

    params = {
        'api-version': '3.0',
        'to': target_language
    }

    body = [{'text': text_to_translate}]

    request = requests.post(constructed_url, params=params, headers=headers, json=body)
    response = request.json()

    if request.status_code == 200 and response:
        # The response is a list, and each item has 'translations' which is also a list.
        # We are interested in the 'text' of the first translation.
        translated_text = response[0]['translations'][0]['text']
        return translated_text
    else:
        return f"Error translating: {response}"
