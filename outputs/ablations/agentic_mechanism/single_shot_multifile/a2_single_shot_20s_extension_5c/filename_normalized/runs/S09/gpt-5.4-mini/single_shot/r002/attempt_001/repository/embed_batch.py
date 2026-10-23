import os
from typing import List

from embeddings_client import create_embeddings_client
from embeddings_models import BatchEmbeddingRequest, extract_embeddings, normalize_texts


def embed_batch(texts: List[str], model: str | None = None) -> List[List[float]]:
    client = create_embeddings_client()
    req = BatchEmbeddingRequest(inputs=normalize_texts(texts), model=model or os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small"))
    response = client.create_embeddings(req)
    return extract_embeddings(response)
