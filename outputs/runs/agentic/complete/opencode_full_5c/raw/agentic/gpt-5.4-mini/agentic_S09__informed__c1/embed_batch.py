from embeddings_client import embed_input
from embeddings_models import normalize_embeddings


def embed_batch(texts):
    response = embed_input(list(texts))
    return normalize_embeddings(item.embedding for item in response.data)
