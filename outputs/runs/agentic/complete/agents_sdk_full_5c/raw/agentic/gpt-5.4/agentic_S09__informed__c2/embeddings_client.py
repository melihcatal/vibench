from __future__ import annotations

import os
from typing import Iterable

from openai import OpenAI

from embeddings_models import EmbeddingRequest, EmbeddingResponse, normalize_text, normalize_texts


OPENAI_EMBEDDING_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")
OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL")


def get_embeddings_client() -> OpenAI:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required for OpenAI embeddings")
    kwargs: dict[str, str] = {"api_key": api_key}
    if OPENAI_BASE_URL:
        kwargs["base_url"] = OPENAI_BASE_URL
    return OpenAI(**kwargs)


def create_embedding(text: str, *, model: str | None = None, dimensions: int | None = None) -> EmbeddingResponse:
    client = get_embeddings_client()
    request = EmbeddingRequest(
        input=normalize_text(text),
        model=model or OPENAI_EMBEDDING_MODEL,
        dimensions=dimensions,
    )
    response = client.embeddings.create(**request.to_openai_kwargs())
    return EmbeddingResponse.from_openai_response(response)


def create_embeddings(texts: Iterable[str], *, model: str | None = None, dimensions: int | None = None) -> EmbeddingResponse:
    client = get_embeddings_client()
    request = EmbeddingRequest(
        input=normalize_texts(texts),
        model=model or OPENAI_EMBEDDING_MODEL,
        dimensions=dimensions,
    )
    response = client.embeddings.create(**request.to_openai_kwargs())
    return EmbeddingResponse.from_openai_response(response)
