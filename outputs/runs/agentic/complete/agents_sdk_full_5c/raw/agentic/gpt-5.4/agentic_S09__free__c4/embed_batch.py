from __future__ import annotations

from embeddings_client import DEFAULT_EMBEDDING_MODEL, create_embeddings
from embeddings_models import BatchEmbeddingRequest, EmbeddingResult, parse_embedding_response_item


def embed_batch(texts: list[str], model: str = DEFAULT_EMBEDDING_MODEL) -> list[EmbeddingResult]:
    request = BatchEmbeddingRequest(texts=texts, model=model)
    normalized_inputs = request.normalized_inputs()
    response = create_embeddings(normalized_inputs, model=request.model)
    return [
        parse_embedding_response_item(item, source_text=normalized_inputs[item.get("index", 0)])
        for item in response["data"]
    ]
