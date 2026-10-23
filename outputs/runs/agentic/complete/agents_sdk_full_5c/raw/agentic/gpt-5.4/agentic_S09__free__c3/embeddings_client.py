from __future__ import annotations

import os
from typing import Sequence

from openai import OpenAI

from embeddings_models import EmbeddingResult, normalize_text, normalize_texts

DEFAULT_EMBEDDING_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")


def get_openai_client() -> OpenAI:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required for the OpenAI embeddings API")
    base_url = os.getenv("OPENAI_BASE_URL")
    if base_url:
        return OpenAI(api_key=api_key, base_url=base_url)
    return OpenAI(api_key=api_key)


def create_embedding(text: str, model: str = DEFAULT_EMBEDDING_MODEL) -> EmbeddingResult:
    client = get_openai_client()
    normalized = normalize_text(text)
    response = client.embeddings.create(model=model, input=normalized)
    vectors = [item.embedding for item in response.data]
    usage = getattr(response, "usage", None)
    usage_dict = usage.model_dump() if usage and hasattr(usage, "model_dump") else None
    return EmbeddingResult(model=response.model, vectors=vectors, usage=usage_dict)


def create_embeddings(texts: Sequence[str], model: str = DEFAULT_EMBEDDING_MODEL) -> EmbeddingResult:
    client = get_openai_client()
    normalized = normalize_texts(texts)
    response = client.embeddings.create(model=model, input=normalized)
    vectors = [item.embedding for item in response.data]
    usage = getattr(response, "usage", None)
    usage_dict = usage.model_dump() if usage and hasattr(usage, "model_dump") else None
    return EmbeddingResult(model=response.model, vectors=vectors, usage=usage_dict)
