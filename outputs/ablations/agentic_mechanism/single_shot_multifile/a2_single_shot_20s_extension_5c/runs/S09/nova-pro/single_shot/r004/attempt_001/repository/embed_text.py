import os
from embeddings_client import get_embeddings_client

def embed_text(text):
    client = get_embeddings_client()
    response = client.embed_text(text)
    return response['embedding']