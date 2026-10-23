import os
from typing import List

from embeddings_client import create_embeddings_client
from embeddings_models import EmbeddingRequest, extract_single_embedding, normalize_text


def embed_text(text: str, model: str | None = None) -> List[float]:
    client = create_embeddings_client()
    req = EmbeddingRequest(input=normalize_text(text), model=model or os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small"))
    response = client.create_embedding(req)
    return extract_single_embedding(response)
