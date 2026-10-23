import os

from openai import OpenAI


def caption_embedding(payload, config=None):
    config = config or {}
    client = OpenAI(api_key=config.get('api_key') or os.environ.get('OPENAI_API_KEY'))
    text = ' '.join(payload.get('chunks', []))
    response = client.embeddings.create(model='text-embedding-3-small', input=text)
    return response.data[0].embedding
