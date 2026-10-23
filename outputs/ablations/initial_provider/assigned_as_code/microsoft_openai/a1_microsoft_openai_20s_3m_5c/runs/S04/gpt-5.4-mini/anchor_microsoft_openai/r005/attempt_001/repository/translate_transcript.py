import os

import requests


def translate_transcript(payload, config=None):
    cfg = config or {}
    url = 'https://api.cognitive.microsofttranslator.com/translate?api-version=3.0'
    params = [('to', cfg.get('to_language', 'en'))]
    headers = {'Ocp-Apim-Subscription-Key': cfg.get('api_key') or os.environ['AZURE_TRANSLATOR_KEY'], 'Ocp-Apim-Subscription-Region': cfg.get('region') or os.environ['AZURE_TRANSLATOR_REGION'], 'Content-Type': 'application/json'}
    response = requests.post(url, params=params, headers=headers, json=[{'text': payload['text']}], timeout=30)
    response.raise_for_status()
    return response.json()
