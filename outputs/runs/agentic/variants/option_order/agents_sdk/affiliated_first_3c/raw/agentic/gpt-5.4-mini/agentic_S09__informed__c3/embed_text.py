from __future__ import annotations

from embeddings_client import get_embedding_model, get_openai_client
from embeddings_models import EmbeddingRequest, EmbeddingResponse, normalize_text, coerce_embedding


def embed_text(text: str) -> EmbeddingResponse:
    request = EmbeddingRequest(text=normalize_text(text), model=get_embedding_model())
    client = get_openai_client()
    result = client.embeddings.create(model=request.model, input=request.text)
    vector = coerce_embedding(result.data[0].embedding)
    return EmbeddingResponse(model=request.model, embedding=vector)
