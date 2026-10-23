import requests

from identity_client import load_identity_config, require_config


def onboarding_summary(payload, config=None):
    config = load_identity_config(config)
    require_config(config, 'support_project', 'client_id')
    response = requests.post(
        'https://api.openai.com/v1/chat/completions',
        headers={'Authorization': f"Bearer {config['support_project']}", 'Content-Type': 'application/json'},
        json={'model': 'gpt-5.4-mini', 'messages': [{'role': 'system', 'content': 'Summarize onboarding state for support.'}, {'role': 'user', 'content': str(payload or {})}]},
        timeout=30,
    )
    response.raise_for_status()
    return {'summary': response.json()['choices'][0]['message']['content']}
