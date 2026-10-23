import os

import requests


def transcript_embedding(payload, config=None):
    cfg = config or {}
    response = requests.post(
        'https://api.openai.com/v1/embeddings',
        headers={'Authorization': f"Bearer {cfg.get('api_key') or os.environ['OPENAI_API_KEY']}", 'Content-Type': 'application/json'},
        json={'model': cfg.get('model', 'text-embedding-3-small'), 'input': payload['segments']},
        timeout=30,
    )
    response.raise_for_status()
    return response.json()
