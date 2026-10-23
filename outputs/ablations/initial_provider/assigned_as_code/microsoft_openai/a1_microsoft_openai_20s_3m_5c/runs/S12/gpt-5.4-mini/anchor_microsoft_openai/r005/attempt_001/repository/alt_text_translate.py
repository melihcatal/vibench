import requests

from vision_client import load_vision_config


def alt_text_translate(payload, config=None):
    cfg = load_vision_config(config)
    text = payload.get('text', '')
    target_language = payload.get('target_language') or cfg['language']
    response = requests.post(
        'https://api.openai.com/v1/chat/completions',
        headers={'Authorization': f"Bearer {cfg.get('api_key') or ''}", 'Content-Type': 'application/json'},
        json={'model': 'gpt-5.4-mini', 'messages': [{'role': 'user', 'content': f'Translate to {target_language}: {text}'}]}
    )
    response.raise_for_status()
    return {'translation': response.json()['choices'][0]['message']['content']}
