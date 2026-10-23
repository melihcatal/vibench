from typing import List
from embeddings_client import get_embeddings_client
from embeddings_models import normalize_texts


def embed_batch(texts: List[str]) -> List[List[float]]:
    client = get_embeddings_client()
    normalized = normalize_texts(texts)
    response = client.embeddings.create(
        model="text-embedding-3-small", input=normalized
    )
    return [[float(x) for x in emb.embedding] for emb in response.data]
