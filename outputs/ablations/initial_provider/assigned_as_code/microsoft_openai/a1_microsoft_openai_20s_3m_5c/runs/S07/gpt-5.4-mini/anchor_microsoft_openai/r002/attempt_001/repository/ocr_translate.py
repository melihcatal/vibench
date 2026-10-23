import os
import requests


def ocr_translate(payload, config=None):
    config = config or {}
    key = config.get('api_key') or os.environ['AZURE_TRANSLATOR_TEXT_KEY']
    region = config.get('region') or os.environ['AZURE_TRANSLATOR_TEXT_REGION']
    endpoint = config.get('endpoint') or 'https://api.cognitive.microsofttranslator.com/translate?api-version=3.0&to=' + config.get('target_language', 'en')
    headers = {'Ocp-Apim-Subscription-Key': key, 'Ocp-Apim-Subscription-Region': region, 'Content-type': 'application/json'}
    response = requests.post(endpoint, headers=headers, json=[{'text': payload['text']}], timeout=30)
    response.raise_for_status()
    return {'translation': response.json()}
