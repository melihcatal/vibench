import os
from openai import OpenAI

from embeddings_client import get_embeddings_client


def embedding_job_summary(payload, config=None):
    config = config or {}
    client = get_embeddings_client(config)
    response = client.embeddings.create(model='text-embedding-3-small', input=payload['text'])
    return {'summary': response.data[0].embedding[:10]}