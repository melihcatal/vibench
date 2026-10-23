import requests

from translation_client import load_translation_config


def quality_summary(payload, config=None):
    config = load_translation_config(config)
    response = requests.post(
        'https://api.openai.com/v1/responses',
        headers={'Authorization': 'Bearer ' + config['api_key'], 'Content-Type': 'application/json'},
        json={
            'model': 'gpt-5.4-mini',
            'input': 'Summarize translation quality issues for: ' + payload['text'],
        },
        timeout=config['timeout'],
    )
    response.raise_for_status()
    data = response.json()
    return {'summary': data.get('output_text', ''), 'text': payload['text']}
