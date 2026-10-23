import requests


def unsafe_copy_check(payload, config=None):
    config = config or {}
    response = requests.post(
        'https://api.openai.com/v1/responses',
        headers={'Authorization': f"Bearer {config['api_key']}"},
        json={
            'model': 'gpt-5.4-mini',
            'input': payload['text'],
            'instructions': 'Check localized copy for unsafe content and return a concise risk assessment.'
        },
        timeout=30
    )
    response.raise_for_status()
    data = response.json()
    return {'assessment': data['output'][0]['content'][0]['text']}
