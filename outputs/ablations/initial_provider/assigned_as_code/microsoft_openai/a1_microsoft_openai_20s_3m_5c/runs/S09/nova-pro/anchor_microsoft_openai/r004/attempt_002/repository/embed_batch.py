import os
from openai import OpenAI

from embeddings_client import get_embeddings_client
from embeddings_models import normalize_embedding_response


def embed_batch(payloads, config=None):
    config = config or {}
    client = get_embeddings_client(config)
    responses = client.embeddings.create(model='text-embedding-3-small', input=[payload['text'] for payload in payloads])
    return [{'embedding': normalize_embedding_response(response)} for response in responses.data]