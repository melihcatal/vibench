from __future__ import annotations

from embeddings_client import get_embeddings_client, resolve_embedding_model
from embeddings_models import BatchEmbeddingRequest, ensure_text_list, parse_embedding_response


def embed_batch(texts: list[str], model: str | None = None) -> list[list[float]]:
    request = BatchEmbeddingRequest(input_texts=ensure_text_list(texts), model=resolve_embedding_model(model))
    client = get_embeddings_client()
    response = client.embeddings.create(
        model=request.model,
        input=request.input_texts,
    )
    parsed = parse_embedding_response(response)
    return [item.embedding for item in parsed.data]
