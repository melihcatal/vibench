import os
from openai import OpenAI


def embed_batch(payloads, config=None):
    config = config or {}
    with OpenAI(api_key=config.get('api_key') or os.environ['OPENAI_API_KEY']) as client:
        response = client.embeddings.create(model='text-embedding-3-small', input=[payload['text'] for payload in payloads])
    return [{'embedding': embedding.embedding} for embedding in response.data]