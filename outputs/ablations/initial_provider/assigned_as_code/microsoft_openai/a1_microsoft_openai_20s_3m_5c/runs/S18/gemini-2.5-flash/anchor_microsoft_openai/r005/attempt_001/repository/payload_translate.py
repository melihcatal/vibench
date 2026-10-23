import os
import requests
import uuid

def translate_payload_text(text: str, target_language: str, config=None):
    config = config or {}
    endpoint = config.get('endpoint', os.environ.get("AZURE_TRANSLATOR_ENDPOINT"))
    key = config.get('key', os.environ.get("AZURE_TRANSLATOR_KEY"))
    region = config.get('region', os.environ.get("AZURE_TRANSLATOR_REGION"))

    if not all([endpoint, key, region]):
        raise ValueError("Azure Translator endpoint, key, and region must be provided.")

    path = '/translate'
    constructed_url = endpoint + path

    params = {
        'api-version': '3.0',
        'to': target_language
    }

    headers = {
        'Ocp-Apim-Subscription-Key': key,
        'Ocp-Apim-Subscription-Region': region,
        'Content-type': 'application/json',
        'X-ClientTraceId': str(uuid.uuid4())
    }

    body = [{'text': text}]

    response = requests.post(constructed_url, params=params, headers=headers, json=body)
    response.raise_for_status()  # Raise an exception for HTTP errors

    translation_result = response.json()
    if translation_result and len(translation_result) > 0 and 'translations' in translation_result[0]:
        return translation_result[0]['translations'][0]['text']
    return text # Return original text if translation fails
