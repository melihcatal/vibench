import os
from openai import OpenAI


def embed_output(payload, config=None):
    config = config or {}
    with OpenAI(api_key=config.get('api_key') or os.environ['OPENAI_API_KEY']) as client:
        response = client.embeddings.create(input=payload['text'], model='text-embedding-ada-002')
    return {'embedding': response.data[0].embedding}