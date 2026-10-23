import os

import requests


def live_caption_safety(payload, config=None):
    config = config or {}
    key = config.get('api_key') or os.environ.get('OPENAI_API_KEY')
    if not key:
        raise ValueError('missing OpenAI API key')
    response = requests.post('https://api.openai.com/v1/chat/completions', headers={
        'Authorization': f'Bearer {key}',
        'Content-Type': 'application/json',
    }, json={
        'model': 'gpt-4o-mini',
        'messages': [
            {'role': 'system', 'content': 'Assess transcript text for unsafe content and return a concise verdict.'},
            {'role': 'user', 'content': payload.get('text', '')},
        ],
        'temperature': 0,
    }, timeout=30)
    response.raise_for_status()
    data = response.json()
    return data['choices'][0]['message']['content']
