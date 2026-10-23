from __future__ import annotations

from embeddings_client import get_embeddings_client, resolve_embedding_model
from embeddings_models import EmbeddingRequest, normalize_text, parse_embedding_response


def embed_text(text: str, model: str | None = None) -> list[float]:
    request = EmbeddingRequest(input_text=normalize_text(text), model=resolve_embedding_model(model))
    client = get_embeddings_client()
    response = client.embeddings.create(
        model=request.model,
        input=request.input_text,
    )
    parsed = parse_embedding_response(response)
    return parsed.data[0].embedding
