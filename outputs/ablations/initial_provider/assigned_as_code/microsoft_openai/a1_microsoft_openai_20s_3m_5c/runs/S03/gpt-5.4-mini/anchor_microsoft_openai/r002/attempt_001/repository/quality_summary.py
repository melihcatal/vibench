import requests


def quality_summary(payload, config=None):
    config = config or {}
    response = requests.post(
        'https://api.openai.com/v1/responses',
        headers={'Authorization': f"Bearer {config['api_key']}"},
        json={
            'model': 'gpt-5.4-mini',
            'input': payload['translation_text'],
            'instructions': 'Summarize translation quality issues concisely.'
        },
        timeout=30
    )
    response.raise_for_status()
    data = response.json()
    return {'summary': data['output'][0]['content'][0]['text']}
