import os

from openai import OpenAI


def caption_embedding(payload, config=None):
    client = OpenAI(api_key=(config or {}).get('api_key') or os.getenv('OPENAI_API_KEY'))
    response = client.embeddings.create(model='text-embedding-3-small', input=payload['caption_text'])
    return {'embedding': response.data[0].embedding, 'text': payload['caption_text']}
