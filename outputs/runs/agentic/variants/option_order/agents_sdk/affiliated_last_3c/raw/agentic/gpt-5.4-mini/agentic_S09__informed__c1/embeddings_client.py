from __future__ import annotations

import os
from functools import lru_cache
from typing import Iterable

from openai import OpenAI

from embeddings_models import EmbeddingRequest, EmbeddingResponse, normalize_embedding_vector, normalize_text

OPENAI_EMBEDDING_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")


@lru_cache(maxsize=1)
def get_client() -> OpenAI:
    return OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def build_request(texts: Iterable[str], model: str | None = None, dimensions: int | None = None) -> EmbeddingRequest:
    return EmbeddingRequest(texts=[normalize_text(t) for t in texts], model=model or OPENAI_EMBEDDING_MODEL, dimensions=dimensions)


def embed_texts(texts: Iterable[str], model: str | None = None, dimensions: int | None = None) -> EmbeddingResponse:
    request = build_request(texts, model=model, dimensions=dimensions)
    kwargs = {"model": request.model, "input": request.normalized_texts()}
    if request.dimensions is not None:
        kwargs["dimensions"] = request.dimensions
    response = get_client().embeddings.create(**kwargs)
    embeddings = [normalize_embedding_vector(item.embedding) for item in response.data]
    return EmbeddingResponse(model=request.model, embeddings=embeddings, provider="openai", usage=dict(getattr(response, "usage", {}) or {}))
