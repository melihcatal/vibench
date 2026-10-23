import os
import requests


def dashboard_note_translate(payload, config=None):
    config = dict(config or {})
    api_key = config.get('api_key') or os.environ['OPENAI_API_KEY']
    source = payload.get('text', '')
    target_language = payload.get('target_language', 'en')
    response = requests.post(
        'https://api.openai.com/v1/chat/completions',
        headers={'Authorization': f'Bearer {api_key}', 'Content-Type': 'application/json'},
        json={
            'model': 'gpt-5.4-mini',
            'messages': [
                {'role': 'system', 'content': 'Translate monitoring notes.'},
                {'role': 'user', 'content': f'Translate this text to {target_language}: {source}'},
            ],
        },
        timeout=30,
    )
    response.raise_for_status()
    return {'text': response.json()['choices'][0]['message']['content']}
