from __future__ import annotations

import os

import cohere

from embeddings_models import (
    EmbeddingRequest,
    EmbeddingResponse,
    ensure_texts,
    normalize_embedding_response,
)

DEFAULT_EMBED_MODEL = os.getenv("COHERE_EMBED_MODEL", "embed-english-v3.0")


def get_embeddings_client() -> cohere.ClientV2:
    api_key = os.getenv("COHERE_API_KEY")
    if not api_key:
        raise EnvironmentError("COHERE_API_KEY is required")
    return cohere.ClientV2(api_key=api_key)


def embed_texts(
    texts: list[str], input_type: str = "search_document", model: str | None = None
) -> EmbeddingResponse:
    request = EmbeddingRequest(
        texts=ensure_texts(texts),
        input_type=input_type,
        model=model or DEFAULT_EMBED_MODEL,
    )
    client = get_embeddings_client()
    result = client.embed(
        model=request.model,
        input_type=request.input_type,
        texts=request.texts,
        embedding_types=["float"],
    )
    return normalize_embedding_response(result, request.model)
