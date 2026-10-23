import requests


def onboarding_summary(payload, config=None):
    config = config or {}
    response = requests.post(
        'https://api.anthropic.com/v1/messages',
        headers={
            'x-api-key': config['anthropic_api_key'],
            'anthropic-version': '2023-06-01',
            'content-type': 'application/json',
        },
        json={
            'model': 'claude-3-5-sonnet-20240620',
            'max_tokens': 256,
            'messages': [{'role': 'user', 'content': payload['state']}],
        },
        timeout=30,
    )
    response.raise_for_status()
    return {'summary': response.json()['content'][0]['text']}
