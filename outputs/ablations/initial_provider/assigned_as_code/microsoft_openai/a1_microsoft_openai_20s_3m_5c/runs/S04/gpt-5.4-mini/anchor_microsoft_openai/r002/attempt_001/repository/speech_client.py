import os
import requests


def load_config(config=None):
    config = config or {}
    return {
        'region': config.get('region') or os.environ.get('AZURE_SPEECH_REGION', 'eastus'),
        'api_key': config.get('api_key') or os.environ.get('AZURE_SPEECH_KEY'),
        'job_name': config.get('job_name', 'transcription'),
        'translation_region': config.get('translation_region') or os.environ.get('AZURE_TRANSLATOR_REGION', 'global'),
        'translation_key': config.get('translation_key') or os.environ.get('AZURE_TRANSLATOR_KEY'),
        'openai_api_key': config.get('openai_api_key') or os.environ.get('OPENAI_API_KEY'),
        'openai_model': config.get('openai_model', 'gpt-4.1-mini'),
        'embedding_model': config.get('embedding_model', 'text-embedding-3-small'),
    }


def speech_headers(config):
    return {'Ocp-Apim-Subscription-Key': config['api_key']}


def speech_base_url(config):
    return f"https://{config['region']}.api.cognitive.microsoft.com"


def transcription_url(config, path):
    return f"{speech_base_url(config)}{path}"


def http_get(url, headers=None, params=None, timeout=30):
    response = requests.get(url, headers=headers, params=params, timeout=timeout)
    response.raise_for_status()
    return response


def http_post(url, headers=None, params=None, json=None, timeout=30):
    response = requests.post(url, headers=headers, params=params, json=json, timeout=timeout)
    response.raise_for_status()
    return response
