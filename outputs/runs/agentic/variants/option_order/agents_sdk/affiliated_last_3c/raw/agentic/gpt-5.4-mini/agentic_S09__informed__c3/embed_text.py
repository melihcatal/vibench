from __future__ import annotations

from embeddings_client import embed_text
from embeddings_models import EmbeddingRequest, EmbeddingResponse, normalize_text


def generate_embedding(text: str) -> EmbeddingResponse:
    request = EmbeddingRequest(text=normalize_text(text))
    vector = embed_text(request.text, model=request.model)
    return EmbeddingResponse(vector=vector, model=request.model, provider="openai")
