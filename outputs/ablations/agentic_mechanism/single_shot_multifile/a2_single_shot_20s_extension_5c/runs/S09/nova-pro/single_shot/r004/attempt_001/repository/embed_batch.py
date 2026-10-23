import os
from embeddings_client import get_embeddings_client

def embed_batch(texts):
    client = get_embeddings_client()
    response = client.embed_batch(texts)
    return response['embeddings']