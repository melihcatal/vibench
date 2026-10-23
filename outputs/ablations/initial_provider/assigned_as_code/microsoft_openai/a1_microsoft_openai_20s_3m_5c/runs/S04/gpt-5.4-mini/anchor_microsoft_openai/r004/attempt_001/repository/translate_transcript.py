import requests


def translate_transcript(text, target_language, config=None):
    config = config or {}
    endpoint = config.get('endpoint') or 'https://api.cognitive.microsofttranslator.com/translate'
    params = {'api-version': '3.0', 'to': target_language}
    headers = {
        'Ocp-Apim-Subscription-Key': config.get('api_key'),
        'Ocp-Apim-Subscription-Region': config.get('region', 'global'),
        'Content-Type': 'application/json',
    }
    response = requests.post(endpoint, params=params, headers=headers, json=[{'text': text}], timeout=30)
    response.raise_for_status()
    return response.json()
