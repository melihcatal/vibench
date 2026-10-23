from __future__ import annotations

from embeddings_client import embed_texts
from embeddings_models import EmbeddingBatchRequest, EmbeddingBatchResponse, normalize_texts


def generate_embeddings(texts: list[str]) -> EmbeddingBatchResponse:
    request = EmbeddingBatchRequest(texts=normalize_texts(texts))
    vectors = embed_texts(request.texts, model=request.model)
    return EmbeddingBatchResponse(vectors=vectors, model=request.model, provider="openai")
