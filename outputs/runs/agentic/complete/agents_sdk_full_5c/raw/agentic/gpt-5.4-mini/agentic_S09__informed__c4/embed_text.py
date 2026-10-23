from __future__ import annotations

from embeddings_client import get_embedding_model, get_openai_client
from embeddings_models import EmbeddingRequest, EmbeddingResponse, normalize_vector


def embed_text(text: str, model: str | None = None) -> EmbeddingResponse:
    client = get_openai_client()
    resolved_model = model or get_embedding_model()
    request = EmbeddingRequest(input_text=text, model=resolved_model)
    response = client.embeddings.create(model=request.model, input=request.input_text)
    vector = normalize_vector(response.data[0].embedding)
    return EmbeddingResponse(vector=vector, model=resolved_model)
