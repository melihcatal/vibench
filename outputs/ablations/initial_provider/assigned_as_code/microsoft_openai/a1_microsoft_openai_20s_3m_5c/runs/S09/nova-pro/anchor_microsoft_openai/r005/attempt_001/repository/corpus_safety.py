import os
from openai import OpenAI

from embeddings_client import get_embeddings_client


def corpus_safety(payload, config=None):
    config = config or {}
    client = get_embeddings_client(config)
    response = client.embeddings.create(model='text-embedding-3-small', input=payload['text'])
    return {'is_safe': len(response.data[0].embedding) > 0}