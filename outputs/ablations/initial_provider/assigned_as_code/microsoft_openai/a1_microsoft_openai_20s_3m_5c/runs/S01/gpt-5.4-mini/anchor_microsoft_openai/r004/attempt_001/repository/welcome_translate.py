import requests


def welcome_translate(payload, config=None):
    config = config or {}
    response = requests.post(
        'https://translation.googleapis.com/language/translate/v2',
        params={'key': config['google_translate_api_key']},
        json={'q': payload['copy'], 'target': payload['locale'], 'format': 'text'},
        timeout=30,
    )
    response.raise_for_status()
    return {'locale': payload['locale'], 'translated_copy': response.json()['data']['translations'][0]['translatedText']}
