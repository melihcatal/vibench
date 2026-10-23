from __future__ import annotations

import os
from typing import Any

from openai import OpenAI

from embeddings_models import BatchEmbeddingRequest, EmbeddingRequest, EmbeddingResponse


DEFAULT_EMBEDDING_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")
DEFAULT_BASE_URL = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")


def get_openai_client() -> OpenAI:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required.")
    return OpenAI(api_key=api_key, base_url=DEFAULT_BASE_URL)


def embed_text_request(text: str, model: str | None = None, dimensions: int | None = None) -> EmbeddingResponse:
    request = EmbeddingRequest(text=text, model=model or DEFAULT_EMBEDDING_MODEL, dimensions=dimensions)
    client = get_openai_client()
    response = client.embeddings.create(**request.to_payload())
    return EmbeddingResponse.from_openai_dict(response.model_dump())


def embed_batch_request(texts: list[str], model: str | None = None, dimensions: int | None = None) -> EmbeddingResponse:
    request = BatchEmbeddingRequest(texts=texts, model=model or DEFAULT_EMBEDDING_MODEL, dimensions=dimensions)
    client = get_openai_client()
    response = client.embeddings.create(**request.to_payload())
    return EmbeddingResponse.from_openai_dict(response.model_dump())


def response_metadata(response: EmbeddingResponse) -> dict[str, Any]:
    return {
        "provider": "OpenAI",
        "base_url": DEFAULT_BASE_URL,
        "model": response.model,
        "embedding_count": len(response.data),
        "usage": response.usage,
    }
