import requests


def transcript_embedding(texts, config=None):
    config = config or {}
    endpoint = config.get('endpoint') or 'https://api.openai.com/v1/embeddings'
    headers = {'Authorization': f"Bearer {config.get('api_key')}", 'Content-Type': 'application/json'}
    response = requests.post(endpoint, headers=headers, json={'model': config.get('model', 'text-embedding-3-large'), 'input': texts}, timeout=30)
    response.raise_for_status()
    return response.json()
