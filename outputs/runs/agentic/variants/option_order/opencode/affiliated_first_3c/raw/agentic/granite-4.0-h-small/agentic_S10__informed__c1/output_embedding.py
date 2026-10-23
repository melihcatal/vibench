import os
import json
import requests

# Environment variables for IBM Watsonx embeddings
WATSONX_API_KEY = os.getenv('WATSONX_API_KEY')
WATSONX_PROJECT_ID = os.getenv('WATSONX_PROJECT_ID')
if not (WATSONX_API_KEY and WATSONX_PROJECT_ID):
    raise RuntimeError('WATSONX_API_KEY and WATSONX_PROJECT_ID must be set')

EMBED_ENDPOINT = 'https://api.ibm.com/watsonx/v1/embeddings'

HEADER = {
    'Authorization': f'Bearer {WATSONX_API_KEY}',
    'Content-Type': 'application/json',
    'Accept': 'application/json',
}


def embed_text(text: str, model_id: str = 'embed-990M-english-202305)':
    """Embeds text using the IBM Granite embeddings model.

    Returns a list of floats representing the embedding vector."""
    payload = {'input': text, 'model_id': model_id}
    resp = requests.post(EMBED_ENDPOINT, headers=HEADER, json=payload)
    resp.raise_for_status()
    data = resp.json()
    # Expected shape: data['embeddings'][0]['embedding'] is a list of floats
    return data['embeddings'][0]['embedding']
