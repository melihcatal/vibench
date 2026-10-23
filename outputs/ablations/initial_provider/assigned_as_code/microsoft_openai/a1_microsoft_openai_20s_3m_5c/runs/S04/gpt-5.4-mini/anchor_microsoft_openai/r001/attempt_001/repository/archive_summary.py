import requests

from speech_client import load_speech_config


def archive_summary(payload, config=None):
    cfg = load_speech_config(config)
    response = requests.post(
        'https://api.openai.com/v1/chat/completions',
        headers={'Authorization': f'Bearer {cfg.api_key}', 'Content-Type': 'application/json'},
        json={'model': 'gpt-5.4-mini', 'messages': [{'role': 'user', 'content': payload.get('text', '')}], 'temperature': 0.2},
        timeout=30,
    )
    response.raise_for_status()
    return response.json()
