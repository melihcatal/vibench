from __future__ import annotations

from embeddings_client import get_embedding_model, get_openai_client
from embeddings_models import EmbeddingBatchRequest, EmbeddingBatchResponse, normalize_vector


def embed_batch(texts: list[str], model: str | None = None) -> EmbeddingBatchResponse:
    client = get_openai_client()
    resolved_model = model or get_embedding_model()
    request = EmbeddingBatchRequest(texts=texts, model=resolved_model)
    response = client.embeddings.create(model=request.model, input=list(request.texts))
    vectors = [normalize_vector(item.embedding) for item in response.data]
    return EmbeddingBatchResponse(vectors=vectors, model=resolved_model)
