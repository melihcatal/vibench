import os
import requests


def load_translation_config(config=None):
    config = config or {}
    return {'api_key': config.get('api_key', os.environ.get('AZURE_TRANSLATOR_KEY')), 'region': config.get('region', os.environ.get('AZURE_TRANSLATOR_REGION', 'global'))}


def translate_with_microsoft(payload, config=None, text_items=None, extra_params=None):
    cfg = load_translation_config(config)
    params = {'api-version': '3.0', 'from': payload['source_language'], 'to': payload['target_language']}
    if extra_params:
        params.update(extra_params)
    body = text_items if text_items is not None else [{'Text': payload['text']}]
    response = requests.post('https://api.cognitive.microsofttranslator.com/translate', headers={'Ocp-Apim-Subscription-Key': cfg['api_key'], 'Ocp-Apim-Subscription-Region': cfg['region']}, params=params, json=body, timeout=30)
    response.raise_for_status()
    return response


def extract_single_translation(response_json):
    return response_json[0]['translations'][0]['text']


def extract_translations(response_json):
    return [item['translations'][0]['text'] for item in response_json]
