import os

import requests


def meeting_summary(payload, config=None):
    config = config or {}
    key = config.get('api_key') or os.environ.get('OPENAI_API_KEY')
    if not key:
        raise ValueError('missing OpenAI API key')
    transcript = '\n'.join(payload.get('chunks', []))
    response = requests.post('https://api.openai.com/v1/chat/completions', headers={
        'Authorization': f'Bearer {key}',
        'Content-Type': 'application/json',
    }, json={
        'model': 'gpt-4o-mini',
        'messages': [
            {'role': 'system', 'content': 'Summarize live meeting transcript chunks into concise notes.'},
            {'role': 'user', 'content': transcript},
        ],
        'temperature': 0.2,
    }, timeout=30)
    response.raise_for_status()
    return response.json()['choices'][0]['message']['content']
