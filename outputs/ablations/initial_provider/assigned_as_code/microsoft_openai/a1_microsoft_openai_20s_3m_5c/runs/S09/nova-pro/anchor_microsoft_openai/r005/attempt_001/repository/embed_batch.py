import os
from openai import OpenAI

from embeddings_client import get_embeddings_client
from embeddings_models import normalize_embedding_response


def embed_batch(payload, config=None):
    config = config or {}
    client = get_embeddings_client(config)
    response = client.embeddings.create(model='text-embedding-3-small', input=payload['texts'])
    embeddings = [normalize_embedding_response(emb) for emb in response.data]
    return {'embeddings': embeddings}