import os
from embeddings_client import DirectEmbeddingsClient

client = DirectEmbeddingsClient()

def embed_batch(texts):
    return client.generate_batch_embeddings(texts)