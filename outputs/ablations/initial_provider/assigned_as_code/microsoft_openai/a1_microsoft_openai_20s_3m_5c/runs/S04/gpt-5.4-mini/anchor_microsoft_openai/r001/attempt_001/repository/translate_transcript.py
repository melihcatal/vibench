import requests

from speech_client import load_speech_config


def translate_transcript(payload, config=None):
    cfg = load_speech_config(config)
    response = requests.post(
        'https://api.cognitive.microsofttranslator.com/translate',
        params={'api-version': '3.0', 'to': payload.get('target_language', 'en')},
        headers={'Ocp-Apim-Subscription-Key': cfg.api_key, 'Ocp-Apim-Subscription-Region': cfg.region, 'Content-Type': 'application/json'},
        json=[{'text': segment['text']} for segment in payload.get('segments', [])],
        timeout=30,
    )
    response.raise_for_status()
    return response.json()
