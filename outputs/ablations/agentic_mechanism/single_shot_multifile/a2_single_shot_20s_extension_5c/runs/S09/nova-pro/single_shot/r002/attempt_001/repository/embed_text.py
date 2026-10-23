import os
from embeddings_client import DirectEmbeddingsClient

client = DirectEmbeddingsClient()

def embed_text(text):
    return client.generate_embedding(text)