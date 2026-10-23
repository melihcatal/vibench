import requests


def translation_memory_embedding(payload, config=None):
    config = config or {}
    response = requests.post(
        'https://api.openai.com/v1/embeddings',
        headers={'Authorization': f"Bearer {config['api_key']}"},
        json={
            'model': 'text-embedding-3-small',
            'input': payload['segments']
        },
        timeout=30
    )
    response.raise_for_status()
    data = response.json()
    return {'embeddings': [item['embedding'] for item in data['data']]}
