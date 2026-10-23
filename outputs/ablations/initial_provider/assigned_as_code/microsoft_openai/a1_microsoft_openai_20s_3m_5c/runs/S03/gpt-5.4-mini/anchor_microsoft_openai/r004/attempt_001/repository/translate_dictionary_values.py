import requests

from translation_client import load_translation_config, translation_headers, translation_url


def translate_dictionary_values(payload, config=None):
    config = load_translation_config(config)
    keys = list(payload['items'].keys())
    values = [payload['items'][key] for key in keys]
    response = requests.post(
        translation_url(config, '/translate'),
        headers=translation_headers(config),
        params={'api-version': '3.0', 'from': payload['source_language'], 'to': payload['target_language']},
        json=[{'Text': str(value)} for value in values],
        timeout=config['timeout'],
    )
    response.raise_for_status()
    translated_values = [item['translations'][0]['text'] for item in response.json()]
    return {
        'items': dict(zip(keys, translated_values)),
        'source_language': payload['source_language'],
        'target_language': payload['target_language'],
    }
