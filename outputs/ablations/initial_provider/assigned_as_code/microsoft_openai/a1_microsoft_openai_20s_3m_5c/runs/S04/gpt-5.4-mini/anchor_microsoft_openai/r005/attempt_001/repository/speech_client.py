import os

import requests


def load_config(config=None):
    config = config or {}
    return {
        'region': config.get('region') or os.environ['AZURE_SPEECH_REGION'],
        'api_key': config.get('api_key') or os.environ['AZURE_SPEECH_KEY'],
        'api_version': config.get('api_version', '2024-11-15'),
        'job_name': config.get('job_name', 'transcription'),
    }


def speech_headers(config):
    return {'Ocp-Apim-Subscription-Key': config['api_key']}


def speech_base_url(config):
    return f"https://{config['region']}.api.cognitive.microsoft.com/speechtotext"


def speech_get(path, config=None, params=None, timeout=30):
    cfg = load_config(config)
    response = requests.get(f"{speech_base_url(cfg)}{path}", headers=speech_headers(cfg), params=params or {'api-version': cfg['api_version']}, timeout=timeout)
    response.raise_for_status()
    return response.json()


def speech_post(path, config=None, params=None, json=None, timeout=30):
    cfg = load_config(config)
    response = requests.post(f"{speech_base_url(cfg)}{path}", headers=speech_headers(cfg), params=params or {'api-version': cfg['api_version']}, json=json, timeout=timeout)
    response.raise_for_status()
    return response.json()
