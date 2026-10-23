from __future__ import annotations

import os
from typing import Sequence

from openai import OpenAI

from embeddings_models import EmbeddingRequest, EmbeddingResponse, parse_openai_embedding_response


DEFAULT_OPENAI_EMBEDDING_MODEL = "text-embedding-3-small"


def get_openai_client() -> OpenAI:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise EnvironmentError("OPENAI_API_KEY is required for OpenAI embeddings")
    base_url = os.environ.get("OPENAI_BASE_URL")
    if base_url:
        return OpenAI(api_key=api_key, base_url=base_url)
    return OpenAI(api_key=api_key)


def create_embedding_request(
    texts: Sequence[str],
    *,
    model: str = DEFAULT_OPENAI_EMBEDDING_MODEL,
    dimensions: int | None = None,
) -> EmbeddingRequest:
    request = EmbeddingRequest(texts=texts, model=model, dimensions=dimensions)
    normalized = request.normalized_inputs()
    if not normalized:
        raise ValueError("At least one non-empty text value is required")
    return EmbeddingRequest(texts=normalized, model=model, dimensions=dimensions)


def fetch_embeddings(request: EmbeddingRequest) -> EmbeddingResponse:
    client = get_openai_client()
    kwargs = {
        "model": request.model,
        "input": list(request.texts),
    }
    if request.dimensions is not None:
        kwargs["dimensions"] = request.dimensions
    response = client.embeddings.create(**kwargs)
    return parse_openai_embedding_response(response)
