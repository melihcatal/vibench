import os
from openai import OpenAI

from embeddings_client import get_embeddings_client


def multilingual_query_translate(payload, config=None):
    config = config or {}
    client = get_embeddings_client(config)
    response = client.embeddings.create(model='text-embedding-3-small', input=payload['query'])
    return {'translated_query': response.data[0].embedding[:10]}