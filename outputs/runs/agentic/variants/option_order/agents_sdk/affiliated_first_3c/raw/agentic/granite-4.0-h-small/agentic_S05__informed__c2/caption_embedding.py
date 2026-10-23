import os
import asyncio
import requests
from speech_models import RecognitionResponse

# Embedding endpoint for IBM Slate (watsonx.ai text embeddings)
SLATE_EMBED_URL = 'https://api.watsonx.ibm.com/v1/embeddings'
WATSONX_API_KEY = os.getenv('WATSONX_API_KEY')

async def embed_caption_chunk(chunk: str) -> list[float]:
    """Sends a single caption chunk to IBM Slate embeddings API and returns vector."""
    headers = {
        'Authorization': f'Bearer {WATSONX_API_KEY}',
        'Content-Type': 'application/json'
    }
    payload = {
        'input': {
            'text': chunk,
            'model': 'text-embedding-ada-002'  # placeholder model name for demo
        }
    }
    response = requests.post(SLATE_EMBED_URL, json=payload, headers=headers)
    if response.status_code != 200:
        print('Embedding error:', response.status_code, response.text)
        return []
    data = response.json()
    # Expected format: [{'embedding': [0.01, -0.02, ...]}, ...]
    embedding = data['embeddings'][0]['embedding']
    return embedding

# Example integration within a streaming pipeline
# async for caption in caption_stream():
#     vec = await embed_caption_chunk(caption)
#     # Store vec in a vector DB for semantic search
#     print('Embedding shape:', len(vec))
