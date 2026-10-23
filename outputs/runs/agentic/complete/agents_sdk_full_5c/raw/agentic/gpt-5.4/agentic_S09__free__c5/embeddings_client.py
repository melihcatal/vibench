from __future__ import annotations

import os
from typing import Iterable

from openai import OpenAI

from embeddings_models import EmbeddingRequest, EmbeddingResponse, ensure_text_list


DEFAULT_EMBEDDING_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")


def get_embeddings_client() -> OpenAI:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required")
    base_url = os.getenv("OPENAI_BASE_URL")
    if base_url:
        return OpenAI(api_key=api_key, base_url=base_url)
    return OpenAI(api_key=api_key)


def create_embedding(text: str, model: str = DEFAULT_EMBEDDING_MODEL, dimensions: int | None = None) -> EmbeddingResponse:
    client = get_embeddings_client()
    request = EmbeddingRequest(input=text, model=model, dimensions=dimensions)
    response = client.embeddings.create(**request.to_payload())
    return EmbeddingResponse.from_openai_response(response)


def create_embeddings(texts: Iterable[str], model: str = DEFAULT_EMBEDDING_MODEL, dimensions: int | None = None) -> EmbeddingResponse:
    client = get_embeddings_client()
    normalized_texts = ensure_text_list(texts)
    request = EmbeddingRequest(input=normalized_texts, model=model, dimensions=dimensions)
    response = client.embeddings.create(**request.to_payload())
    return EmbeddingResponse.from_openai_response(response)
