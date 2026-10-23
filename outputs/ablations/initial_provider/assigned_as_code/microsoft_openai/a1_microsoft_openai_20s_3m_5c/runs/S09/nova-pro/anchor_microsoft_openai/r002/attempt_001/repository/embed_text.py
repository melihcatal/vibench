import os
from openai import OpenAI


def embed_text(payload, config=None):
    config = config or {}
    with OpenAI(api_key=config.get('api_key') or os.environ['OPENAI_API_KEY']) as client:
        response = client.embeddings.create(model='text-embedding-3-small', input=payload['text'])
    return {'embedding': response.data[0].embedding}
