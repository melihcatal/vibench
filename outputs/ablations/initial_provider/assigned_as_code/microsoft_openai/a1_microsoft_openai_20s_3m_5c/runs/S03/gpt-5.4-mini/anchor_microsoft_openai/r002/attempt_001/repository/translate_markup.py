import requests

from translation_client import get_translation_config
from translation_models import normalize_markup_request, parse_markup_response


def translate_markup(payload, config=None):
    config = get_translation_config(config)
    request = normalize_markup_request(payload)
    response = requests.post(
        'https://api.cognitive.microsofttranslator.com/translate',
        headers={
            'Ocp-Apim-Subscription-Key': config['api_key'],
            'Ocp-Apim-Subscription-Region': config['region']
        },
        params={
            'api-version': '3.0',
            'from': request['source_language'],
            'to': request['target_language'],
            'textType': 'html'
        },
        json=[{'Text': request['markup']}],
        timeout=30
    )
    response.raise_for_status()
    return parse_markup_response(response.json(), request)
