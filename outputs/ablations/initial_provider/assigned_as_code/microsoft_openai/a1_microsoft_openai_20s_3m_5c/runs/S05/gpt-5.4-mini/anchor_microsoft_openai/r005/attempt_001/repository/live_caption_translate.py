import os

import requests


def live_caption_translate(payload, config=None):
    config = config or {}
    key = config.get('api_key') or os.environ.get('OPENAI_API_KEY')
    if not key:
        raise ValueError('missing OpenAI API key')
    target_language = payload.get('target_language', 'es')
    text = payload.get('text', '')
    response = requests.post('https://api.openai.com/v1/chat/completions', headers={
        'Authorization': f'Bearer {key}',
        'Content-Type': 'application/json',
    }, json={
        'model': 'gpt-4o-mini',
        'messages': [
            {'role': 'system', 'content': f'Translate live captions to {target_language}.'},
            {'role': 'user', 'content': text},
        ],
        'temperature': 0,
    }, timeout=30)
    response.raise_for_status()
    data = response.json()
    return data['choices'][0]['message']['content']
