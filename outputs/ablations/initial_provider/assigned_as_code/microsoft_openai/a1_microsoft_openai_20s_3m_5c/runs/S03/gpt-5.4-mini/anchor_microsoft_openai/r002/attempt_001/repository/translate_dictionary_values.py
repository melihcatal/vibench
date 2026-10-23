import requests

from translation_client import get_translation_config
from translation_models import normalize_dictionary_request, parse_dictionary_response


def translate_dictionary_values(payload, config=None):
    config = get_translation_config(config)
    request = normalize_dictionary_request(payload)
    items = list(request['mapping'].items())
    response = requests.post(
        'https://api.cognitive.microsofttranslator.com/translate',
        headers={
            'Ocp-Apim-Subscription-Key': config['api_key'],
            'Ocp-Apim-Subscription-Region': config['region']
        },
        params={
            'api-version': '3.0',
            'from': request['source_language'],
            'to': request['target_language']
        },
        json=[{'Text': value} for _, value in items],
        timeout=30
    )
    response.raise_for_status()
    return parse_dictionary_response(response.json(), items, request)
