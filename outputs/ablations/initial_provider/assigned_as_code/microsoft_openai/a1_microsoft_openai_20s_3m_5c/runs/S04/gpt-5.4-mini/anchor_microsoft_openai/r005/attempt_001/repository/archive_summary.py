import os

import requests


def archive_summary(payload, config=None):
    cfg = config or {}
    response = requests.post(
        'https://api.openai.com/v1/chat/completions',
        headers={'Authorization': f"Bearer {cfg.get('api_key') or os.environ['OPENAI_API_KEY']}", 'Content-Type': 'application/json'},
        json={'model': cfg.get('model', 'gpt-4.1-mini'), 'messages': [{'role': 'user', 'content': f"Summarize this transcript:\n{payload['transcript']}"}], 'temperature': 0.2},
        timeout=30,
    )
    response.raise_for_status()
    return response.json()
