import requests

from speech_client import load_speech_config


def moderate_transcript(payload, config=None):
    cfg = load_speech_config(config)
    response = requests.post(
        'https://api.openai.com/v1/moderations',
        headers={'Authorization': f'Bearer {cfg.api_key}', 'Content-Type': 'application/json'},
        json={'model': 'omni-moderation-latest', 'input': payload.get('text', '')},
        timeout=30,
    )
    response.raise_for_status()
    return response.json()
