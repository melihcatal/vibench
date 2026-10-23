import os
import requests


def load_config(config=None):
    config = config or {}
    return {
        'region': config.get('region') or os.environ.get('AZURE_SPEECH_REGION', 'eastus'),
        'api_key': config.get('api_key') or os.environ.get('AZURE_SPEECH_KEY'),
        'job_name': config.get('job_name') or 'transcription',
        'language': config.get('language') or config.get('language_code') or 'en-US',
        'output_format': config.get('output_format') or 'simple',
        'features': config.get('features') or [],
    }


def speech_base_url(region):
    return f'https://{region}.api.cognitive.microsoft.com/speechtotext/v3.2'


def auth_headers(config):
    return {'Ocp-Apim-Subscription-Key': config['api_key']}


def request_json(method, url, config, **kwargs):
    response = requests.request(method, url, headers=auth_headers(config), timeout=30, **kwargs)
    response.raise_for_status()
    if response.text:
        return response.json()
    return {}
