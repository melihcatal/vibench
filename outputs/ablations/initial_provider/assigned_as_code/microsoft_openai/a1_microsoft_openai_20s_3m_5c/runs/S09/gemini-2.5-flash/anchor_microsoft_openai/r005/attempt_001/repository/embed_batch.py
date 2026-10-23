import os
from openai import OpenAI


def embed_batch(payload, config=None):
    config = config or {}
    with OpenAI(api_key=config.get('api_key') or os.environ['OPENAI_API_KEY']) as client:
        response = client.embeddings.create(model='text-embedding-3-small', input=payload['texts'])
    return {'embeddings': [item.embedding for item in response.data]}