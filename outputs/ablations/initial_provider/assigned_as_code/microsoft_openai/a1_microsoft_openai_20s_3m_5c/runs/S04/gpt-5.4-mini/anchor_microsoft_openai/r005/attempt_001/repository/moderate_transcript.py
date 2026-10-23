import os

import requests


def moderate_transcript(payload, config=None):
    cfg = config or {}
    response = requests.post(
        'https://api.openai.com/v1/moderations',
        headers={'Authorization': f"Bearer {cfg.get('api_key') or os.environ['OPENAI_API_KEY']}", 'Content-Type': 'application/json'},
        json={'model': cfg.get('model', 'omni-moderation-latest'), 'input': payload['text']},
        timeout=30,
    )
    response.raise_for_status()
    return response.json()
