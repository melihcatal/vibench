from __future__ import annotations

import os
from typing import Any

import cohere

from embeddings_models import (
    EmbeddingRequest,
    EmbeddingResponse,
    normalize_texts,
    parse_cohere_embeddings,
)


DEFAULT_EMBED_MODEL = os.getenv("COHERE_EMBED_MODEL", "embed-v4.0")


def get_cohere_client(api_key: str | None = None) -> cohere.ClientV2:
    key = api_key or os.getenv("COHERE_API_KEY")
    if not key:
        raise RuntimeError("COHERE_API_KEY is required")
    return cohere.ClientV2(api_key=key)


def build_embedding_request(
    texts: list[str], model: str | None = None, input_type: str = "search_document"
) -> EmbeddingRequest:
    normalized = normalize_texts(texts)
    if not normalized:
        raise ValueError("At least one non-empty text is required")
    return EmbeddingRequest(
        texts=normalized, model=model or DEFAULT_EMBED_MODEL, input_type=input_type
    )


def create_embeddings(
    texts: list[str],
    *,
    model: str | None = None,
    input_type: str = "search_document",
    output_dimension: int | None = None,
    api_key: str | None = None,
) -> EmbeddingResponse:
    request = build_embedding_request(texts, model=model, input_type=input_type)
    client = get_cohere_client(api_key=api_key)
    response = client.embed(
        model=request.model,
        input_type=request.input_type,
        texts=request.texts,
        embedding_types=["float"],
        output_dimension=output_dimension,
    )
    payload: dict[str, Any] = (
        response.dict() if hasattr(response, "dict") else dict(response)
    )
    float_embeddings = payload.get("embeddings", {}).get("float")
    if float_embeddings is not None:
        payload = {
            "embeddings": float_embeddings,
            "meta": payload.get("meta", {}),
            "id": request.model,
        }
    return parse_cohere_embeddings(payload, request.texts)
