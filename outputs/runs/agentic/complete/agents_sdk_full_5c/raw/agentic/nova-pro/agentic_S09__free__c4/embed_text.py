from embeddings_client import EmbeddingsClient

client = EmbeddingsClient()

def embed_text(text):
    return client.embed_text(text)