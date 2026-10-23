from __future__ import annotations

import os
from typing import Any

from openai import OpenAI

from embeddings_models import (
    EmbeddingRequest,
    EmbeddingResponse,
    parse_embedding_response,
)

OPENAI_EMBEDDINGS_MODEL = os.getenv("OPENAI_EMBEDDINGS_MODEL", "text-embedding-3-small")


def get_openai_client() -> OpenAI:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required")
    base_url = os.getenv("OPENAI_BASE_URL")
    if base_url:
        return OpenAI(api_key=api_key, base_url=base_url)
    return OpenAI(api_key=api_key)


def create_embeddings(
    input_value: str | list[str],
    model: str | None = None,
    dimensions: int | None = None,
) -> EmbeddingResponse:
    request = EmbeddingRequest(
        model=model or OPENAI_EMBEDDINGS_MODEL, input=input_value, dimensions=dimensions
    )
    client = get_openai_client()
    response = client.embeddings.create(**request.to_payload())
    data: dict[str, Any] = response.model_dump()
    return parse_embedding_response(data, provider="OpenAI")
