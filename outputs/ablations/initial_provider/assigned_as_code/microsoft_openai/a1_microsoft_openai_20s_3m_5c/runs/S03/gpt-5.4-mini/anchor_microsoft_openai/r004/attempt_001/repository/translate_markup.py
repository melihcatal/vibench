import requests

from translation_client import load_translation_config, translation_headers, translation_url


def translate_markup(payload, config=None):
    config = load_translation_config(config)
    response = requests.post(
        translation_url(config, '/translate'),
        headers=translation_headers(config),
        params={'api-version': '3.0', 'from': payload['source_language'], 'to': payload['target_language'], 'textType': 'html'},
        json=[{'Text': payload['markup']}],
        timeout=config['timeout'],
    )
    response.raise_for_status()
    return {
        'markup': response.json()[0]['translations'][0]['text'],
        'source_language': payload['source_language'],
        'target_language': payload['target_language'],
    }
