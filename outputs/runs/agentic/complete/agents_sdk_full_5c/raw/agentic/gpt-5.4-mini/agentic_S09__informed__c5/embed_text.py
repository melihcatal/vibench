from __future__ import annotations

from embeddings_client import get_client, get_model_name
from embeddings_models import EmbeddingRequest, EmbeddingResponse


def embed_text(text: str, model: str | None = None) -> EmbeddingResponse:
    chosen_model = get_model_name(model)
    request = EmbeddingRequest(text=text, model=chosen_model)
    client = get_client()
    result = client.embeddings.create(model=request.model, input=request.text)
    return EmbeddingResponse(model=request.model, embedding=list(result.data[0].embedding))
