from embeddings_client import embed_input
from embeddings_models import normalize_embedding


def embed_text(text: str):
    response = embed_input(text)
    return normalize_embedding(response.data[0].embedding)
