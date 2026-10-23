from __future__ import annotations

from embeddings_client import get_client, load_settings
from embeddings_models import EmbeddingRequest, EmbeddingResponse, normalize_texts, normalize_vector


def embed_batch(texts: list[str]) -> EmbeddingResponse:
    settings = load_settings()
    client = get_client(settings)
    cleaned = normalize_texts(texts)
    request = EmbeddingRequest(inputs=cleaned, model=settings.embedding_model)
    response = client.embeddings.create(model=request.model, input=list(request.inputs))
    vectors = [normalize_vector(item.embedding) for item in response.data]
    return EmbeddingResponse(vectors=vectors, model=request.model)
