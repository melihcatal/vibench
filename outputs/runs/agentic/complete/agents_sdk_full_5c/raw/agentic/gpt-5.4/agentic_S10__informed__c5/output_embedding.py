from __future__ import annotations

import os
from typing import Iterable, List

from openai import OpenAI

from model_models import EmbeddingResponse


DEFAULT_EMBEDDING_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")


def embed_outputs(texts: Iterable[str], model: str | None = None) -> EmbeddingResponse:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required")
    client = OpenAI(api_key=api_key)
    payload: List[str] = list(texts)
    response = client.embeddings.create(
        model=model or DEFAULT_EMBEDDING_MODEL,
        input=payload,
    )
    vectors = [item.embedding for item in response.data]
    dims = len(vectors[0]) if vectors else None
    return EmbeddingResponse(vectors=vectors, model=response.model, dimensions=dims)
