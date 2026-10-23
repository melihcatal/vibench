import os
from openai import OpenAI

from model_client import get_client


def embed_output(payload, config=None):
    client = get_client(config)
    response = client.embeddings.create(input=payload['text'], model='text-embedding-ada-002')
    return {'embedding': response.data[0].embedding}