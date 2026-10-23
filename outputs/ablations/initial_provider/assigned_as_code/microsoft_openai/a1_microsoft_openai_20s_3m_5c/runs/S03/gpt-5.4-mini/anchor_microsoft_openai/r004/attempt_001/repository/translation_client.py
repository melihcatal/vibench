import os

DEFAULT_TIMEOUT = 30


def load_translation_config(config=None):
    config = config or {}
    return {
        'api_key': config.get('api_key') or os.getenv('AZURE_TRANSLATOR_KEY'),
        'region': config.get('region') or os.getenv('AZURE_TRANSLATOR_REGION'),
        'endpoint': config.get('endpoint') or os.getenv('AZURE_TRANSLATOR_ENDPOINT', 'https://api.cognitive.microsofttranslator.com'),
        'timeout': config.get('timeout', DEFAULT_TIMEOUT),
    }


def translation_headers(config):
    return {
        'Ocp-Apim-Subscription-Key': config['api_key'],
        'Ocp-Apim-Subscription-Region': config['region'],
    }


def translation_url(config, path):
    return config['endpoint'].rstrip('/') + path
