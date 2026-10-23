import requests
from speech_client import load_config


def translate_transcript(payload, config=None):
    config = load_config(config)
    texts = [segment.get('text', '') for segment in payload.get('segments', [])]
    response = requests.post(
        f"https://api.cognitive.microsofttranslator.com/translate?api-version=3.0&to={payload.get('target_language', 'en')}",
        headers={'Ocp-Apim-Subscription-Key': config['translation_key'], 'Ocp-Apim-Subscription-Region': config['translation_region'], 'Content-Type': 'application/json'},
        json=[{'text': text} for text in texts],
        timeout=30,
    )
    response.raise_for_status()
    return response.json()
