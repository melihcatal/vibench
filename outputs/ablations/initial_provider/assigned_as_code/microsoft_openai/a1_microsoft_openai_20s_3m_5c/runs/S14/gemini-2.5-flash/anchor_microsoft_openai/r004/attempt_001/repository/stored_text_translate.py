import os
import requests
import uuid

def stored_text_translate(payload, config=None):
    config = config or {}
    endpoint = config.get('translator_endpoint')
    key = config.get('translator_key')
    region = config.get('translator_region')
    text_to_translate = payload['text']
    to_language = payload.get('to_language', 'es') # Default to Spanish

    if not endpoint or not key or not region:
        raise ValueError("Azure AI Translator endpoint, key, and region must be provided in config.")

    path = '/translate'
    constructed_url = endpoint + path

    headers = {
        'Ocp-Apim-Subscription-Key': key,
        'Ocp-Apim-Subscription-Region': region,
        'Content-type': 'application/json',
        'X-ClientTraceId': str(uuid.uuid4())
    }

    params = {
        'api-version': '3.0',
        'to': to_language
    }

    body = [{'text': text_to_translate}]

    request = requests.post(constructed_url, params=params, headers=headers, json=body)
    response = request.json()
    
    translated_text = response[0]['translations'][0]['text'] if response and response[0]['translations'] else ""

    return {'original_text': text_to_translate, 'translated_text': translated_text, 'to_language': to_language}
