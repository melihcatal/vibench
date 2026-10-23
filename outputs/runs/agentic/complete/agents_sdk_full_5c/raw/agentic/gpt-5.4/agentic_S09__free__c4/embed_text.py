from __future__ import annotations

from embeddings_client import DEFAULT_EMBEDDING_MODEL, create_embedding
from embeddings_models import EmbeddingRequest, parse_embedding_response_item


def embed_text(text: str, model: str = DEFAULT_EMBEDDING_MODEL) -> list[float]:
    request = EmbeddingRequest(text=text, model=model)
    response = create_embedding(request.normalized_text(), model=request.model)
    return parse_embedding_response_item(response["data"][0], source_text=request.text).vector
