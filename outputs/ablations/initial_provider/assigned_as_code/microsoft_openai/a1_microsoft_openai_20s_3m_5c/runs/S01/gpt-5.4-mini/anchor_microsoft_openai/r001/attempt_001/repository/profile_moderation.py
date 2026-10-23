import requests

from identity_client import load_identity_config, require_config


def profile_moderation(payload, config=None):
    config = require_config(load_identity_config(config), 'openai_api_key')
    response = requests.post('https://api.openai.com/v1/moderations', headers={'Authorization': 'Bearer ' + config['openai_api_key'], 'Content-Type': 'application/json'}, json={'model': 'omni-moderation-latest', 'input': payload['text']}, timeout=30)
    response.raise_for_status()
    result = response.json()['results'][0]
    return {'flagged': result['flagged'], 'categories': result.get('categories', {})}
