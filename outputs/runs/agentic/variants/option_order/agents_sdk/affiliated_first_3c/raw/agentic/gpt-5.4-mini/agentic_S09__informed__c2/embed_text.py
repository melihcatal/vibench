from __future__ import annotations

from embeddings_client import get_client, get_embedding_model, normalize_input
from embeddings_models import EmbeddingRequest, EmbeddingResponse, coerce_embedding


def embed_text(text: str) -> EmbeddingResponse:
    model = get_embedding_model()
    request = EmbeddingRequest(text=text, model=model)
    client = get_client()
    cleaned = normalize_input([request.text])
    if not cleaned:
        raise ValueError("text must not be empty")
    result = client.embeddings.create(model=request.model, input=cleaned[0])
    item = result.data[0]
    return EmbeddingResponse(
        model=request.model,
        embedding=coerce_embedding(item.embedding),
        usage={"prompt_tokens": getattr(result.usage, "prompt_tokens", None), "total_tokens": getattr(result.usage, "total_tokens", None)},
    )
