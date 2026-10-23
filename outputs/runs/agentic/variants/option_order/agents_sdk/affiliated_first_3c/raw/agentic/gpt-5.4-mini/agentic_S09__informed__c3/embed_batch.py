from __future__ import annotations

from embeddings_client import get_embedding_model, get_openai_client
from embeddings_models import BatchEmbeddingRequest, BatchEmbeddingResponse, normalize_texts, coerce_embedding


def embed_batch(texts: list[str]) -> BatchEmbeddingResponse:
    request = BatchEmbeddingRequest(texts=normalize_texts(texts), model=get_embedding_model())
    client = get_openai_client()
    result = client.embeddings.create(model=request.model, input=request.texts)
    embeddings = [coerce_embedding(item.embedding) for item in result.data]
    return BatchEmbeddingResponse(model=request.model, embeddings=embeddings)
