from embeddings_client import EmbeddingsClient

client = EmbeddingsClient()

def embed_batch(texts):
    return client.embed_batch(texts)