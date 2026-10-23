import os
import requests


def ocr_translate(payload, config=None):
    config = config or {}
    endpoint = config.get('endpoint') or os.environ['AZURE_TRANSLATOR_ENDPOINT']
    key = config.get('api_key') or os.environ['AZURE_TRANSLATOR_TEXT_API_KEY']
    region = config.get('region') or os.environ['AZURE_TRANSLATOR_REGION']
    params = {'api-version': '3.0', 'to': config.get('to_language', 'en')}
    headers = {
        'Ocp-Apim-Subscription-Key': key,
        'Ocp-Apim-Subscription-Region': region,
        'Content-Type': 'application/json',
    }
    body = [{'text': payload['text']}]
    response = requests.post(f'{endpoint}/translate', params=params, headers=headers, json=body, timeout=30)
    response.raise_for_status()
    return {'translations': response.json()}
