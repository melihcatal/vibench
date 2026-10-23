import os


def get_speech_client(config=None):
    config = config or {}
    api_key = config.get('api_key') or os.environ['AZURE_SPEECH_KEY']
    region = config.get('region') or 'westus'
    import requests
    return requests.Session()


def normalize_response(response):
    return response.json()['transcripts'][0]['text'] if response.json()['status'] == 'Succeeded' else None