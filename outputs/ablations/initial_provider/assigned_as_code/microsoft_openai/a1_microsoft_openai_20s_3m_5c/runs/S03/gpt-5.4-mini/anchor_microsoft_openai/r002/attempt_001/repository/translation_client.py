import os


def get_translation_config(config=None):
    config = config or {}
    api_key = config.get('api_key') or os.environ['MICROSOFT_TRANSLATOR_KEY']
    region = config.get('region') or os.environ.get('MICROSOFT_TRANSLATOR_REGION', 'global')
    return {'api_key': api_key, 'region': region}
