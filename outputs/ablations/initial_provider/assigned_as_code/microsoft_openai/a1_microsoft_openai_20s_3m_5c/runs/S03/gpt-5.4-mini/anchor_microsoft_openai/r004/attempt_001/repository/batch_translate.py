import requests

from translation_client import load_translation_config, translation_headers, translation_url
from translation_models import normalize_strings


def batch_translate(payload, config=None):
    config = load_translation_config(config)
    texts = normalize_strings(payload['texts'])
    response = requests.post(
        translation_url(config, '/translate'),
        headers=translation_headers(config),
        params={'api-version': '3.0', 'from': payload['source_language'], 'to': payload['target_language']},
        json=[{'Text': text} for text in texts],
        timeout=config['timeout'],
    )
    response.raise_for_status()
    translated = [item['translations'][0]['text'] for item in response.json()]
    return {
        'texts': translated,
        'source_language': payload['source_language'],
        'target_language': payload['target_language'],
    }
