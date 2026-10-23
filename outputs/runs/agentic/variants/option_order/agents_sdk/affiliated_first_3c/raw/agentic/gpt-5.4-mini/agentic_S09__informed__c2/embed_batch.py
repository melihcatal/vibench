from __future__ import annotations

from embeddings_client import get_client, get_embedding_model, normalize_input
from embeddings_models import BatchEmbeddingRequest, BatchEmbeddingResponse, coerce_embedding


def embed_batch(texts: list[str]) -> BatchEmbeddingResponse:
    model = get_embedding_model()
    request = BatchEmbeddingRequest(texts=texts, model=model)
    client = get_client()
    cleaned = normalize_input(request.texts)
    if not cleaned:
        raise ValueError("texts must contain at least one non-empty item")
    result = client.embeddings.create(model=request.model, input=cleaned)
    embeddings = [coerce_embedding(item.embedding) for item in result.data]
    return BatchEmbeddingResponse(
        model=request.model,
        embeddings=embeddings,
        usage={"prompt_tokens": getattr(result.usage, "prompt_tokens", None), "total_tokens": getattr(result.usage, "total_tokens", None)},
    )
