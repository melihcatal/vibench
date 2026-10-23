import os
from embeddings_client import EmbeddingsClient

client = EmbeddingsClient()

def embed_batch(texts):
    return client.generate_batch_embeddings(texts)