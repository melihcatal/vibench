import requests

from speech_client import load_speech_config


def transcript_embedding(payload, config=None):
    cfg = load_speech_config(config)
    response = requests.post(
        'https://api.openai.com/v1/embeddings',
        headers={'Authorization': f'Bearer {cfg.api_key}', 'Content-Type': 'application/json'},
        json={'model': 'text-embedding-3-small', 'input': [segment['text'] for segment in payload.get('segments', [])]},
        timeout=30,
    )
    response.raise_for_status()
    return response.json()
