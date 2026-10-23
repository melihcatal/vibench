import os
import requests
import uuid

def translate_payload_text(text: str, target_language: str = "es", source_language: str = "en"):
    key = os.environ.get("AZURE_TRANSLATOR_TEXT_SUBSCRIPTION_KEY")
    endpoint = os.environ.get("AZURE_TRANSLATOR_TEXT_ENDPOINT")
    location = os.environ.get("AZURE_TRANSLATOR_TEXT_LOCATION")

    if not key or not endpoint or not location:
        raise ValueError("AZURE_TRANSLATOR_TEXT_SUBSCRIPTION_KEY, AZURE_TRANSLATOR_TEXT_ENDPOINT or AZURE_TRANSLATOR_TEXT_LOCATION environment variables not set.")

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
        'from': source_language,
        'to': [target_language]
    }

    body = [{'text': text}]

    request = requests.post(constructed_url, params=params, headers=headers, json=body)
    response = request.json()

    translated_text = response[0]['translations'][0]['text'] if response and response[0]['translations'] else text

    return {"translated_text": translated_text, "translation_results": response}
