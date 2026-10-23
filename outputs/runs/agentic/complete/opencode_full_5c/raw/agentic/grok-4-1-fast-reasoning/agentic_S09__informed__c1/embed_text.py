from embeddings_client import EmbeddingsClient
from embeddings_models import normalize_embedding
from typing import List


def embed_text(text: str) -> List[float]:
    client = EmbeddingsClient()
    raw_embedding = client.embed_documents([text])[0]
    return normalize_embedding(raw_embedding)
