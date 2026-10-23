import requests

from identity_client import load_identity_config, require_config


def onboarding_summary(payload, config=None):
    config = require_config(load_identity_config(config), 'anthropic_api_key')
    response = requests.post('https://api.anthropic.com/v1/messages', headers={'x-api-key': config['anthropic_api_key'], 'anthropic-version': '2023-06-01', 'content-type': 'application/json'}, json={'model': 'claude-3-5-sonnet-20240620', 'max_tokens': 256, 'messages': [{'role': 'user', 'content': payload['state']}]}, timeout=30)
    response.raise_for_status()
    data = response.json()
    return {'summary': data['content'][0]['text'], 'id': data.get('id')}
