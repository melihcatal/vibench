import os
import requests
from translation_models import load_config
import json

def embed_segments(translated_segments: list[str]):
    """Embed translated segments using Cohere Embed API (general purpose).",
    config = load_config()
    api_key = config.get('COHERE_API_KEY') or os.getenv('COHERE_API_KEY')
    if not api_key:
        raise RuntimeError('COHERE_API_KEY not configured')
    endpoint = 'https://api.cohere.ai/v1/embed'
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }
    data = {
        'texts': translated_segments,
        'model': 'embed-english-light-v3.0'
    }
    resp = requests.post(endpoint, headers=headers, json=data)
    resp.raise_for_status()
    embeddings = resp.json()['embeddings']
    # Return list of embedding vectors as lists of floats
    return [vec['embedding'] for vec in embeddings]
