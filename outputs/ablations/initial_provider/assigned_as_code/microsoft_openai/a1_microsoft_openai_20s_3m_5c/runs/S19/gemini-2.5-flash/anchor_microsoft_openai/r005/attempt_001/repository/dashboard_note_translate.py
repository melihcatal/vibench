import os
import requests
import uuid
import json

def dashboard_note_translate(payload, config=None):
    config = config or {}
    endpoint = os.environ.get("AZURE_TRANSLATOR_TEXT_ENDPOINT")
    subscription_key = os.environ.get("AZURE_TRANSLATOR_TEXT_SUBSCRIPTION_KEY")
    region = os.environ.get("AZURE_TRANSLATOR_TEXT_REGION")

    path = '/translate?api-version=3.0'
    params = f'&to={payload['target_language']}'
    constructed_url = endpoint + path + params

    headers = {
        'Ocp-Apim-Subscription-Key': subscription_key,
        'Ocp-Apim-Subscription-Region': region,
        'Content-type': 'application/json',
        'X-ClientTraceId': str(uuid.uuid4())
    }

    body = [{'text': payload['note_text']}]

    request = requests.post(constructed_url, headers=headers, json=body)
    response = request.json()

    # The response is a list of dictionaries, each containing translations.
    # We expect one translation for the single text we sent.
    if response and len(response) > 0 and 'translations' in response[0]:
        return {'translated_text': response[0]['translations'][0]['text']}
    else:
        return {'translated_text': payload['note_text'], 'error': 'Translation failed or no translations found.'}
