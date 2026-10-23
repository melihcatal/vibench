from __future__ import annotations

import os
from typing import Iterable

from openai import OpenAI

from embeddings_models import EmbeddingRequest, EmbeddingResponse, EmbeddingVector, normalize_texts

DEFAULT_OPENAI_EMBEDDING_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")



def get_embeddings_client() -> OpenAI:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise EnvironmentError("OPENAI_API_KEY is required for OpenAI embeddings")
    return OpenAI(api_key=api_key)



def build_embedding_request(
    texts: Iterable[str],
    model: str | None = None,
    dimensions: int | None = None,
) -> EmbeddingRequest:
    normalized = normalize_texts(texts)
    if not normalized:
        raise ValueError("At least one non-empty text is required")
    return EmbeddingRequest(texts=normalized, model=model or DEFAULT_OPENAI_EMBEDDING_MODEL, dimensions=dimensions)



def create_embeddings(
    texts: Iterable[str],
    model: str | None = None,
    dimensions: int | None = None,
) -> EmbeddingResponse:
    request = build_embedding_request(texts=texts, model=model, dimensions=dimensions)
    client = get_embeddings_client()
    payload: dict[str, object] = {"model": request.model, "input": request.texts}
    if request.dimensions is not None:
        payload["dimensions"] = request.dimensions
    result = client.embeddings.create(**payload)
    vectors = [
        EmbeddingVector(index=item.index, embedding=list(item.embedding), source_text=request.texts[item.index])
        for item in result.data
    ]
    usage = {}
    if getattr(result, "usage", None) is not None:
        usage = {
            key: value
            for key, value in result.usage.model_dump().items()
            if value is not None
        }
    return EmbeddingResponse(model=result.model, vectors=vectors, usage=usage)
