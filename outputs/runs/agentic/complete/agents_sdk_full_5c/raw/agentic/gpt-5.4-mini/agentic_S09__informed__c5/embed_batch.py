from __future__ import annotations

from embeddings_client import get_client, get_model_name
from embeddings_models import BatchEmbeddingRequest, BatchEmbeddingResponse


def embed_batch(texts: list[str], model: str | None = None) -> BatchEmbeddingResponse:
    chosen_model = get_model_name(model)
    request = BatchEmbeddingRequest(texts=texts, model=chosen_model)
    client = get_client()
    result = client.embeddings.create(model=request.model, input=list(request.texts))
    embeddings = [list(item.embedding) for item in result.data]
    return BatchEmbeddingResponse(model=request.model, embeddings=embeddings)
