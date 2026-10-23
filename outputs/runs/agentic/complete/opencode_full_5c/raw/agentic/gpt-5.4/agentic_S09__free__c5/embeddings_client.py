from __future__ import annotations

import os
from typing import Sequence

from openai import OpenAI

from embeddings_models import (
    EmbeddingResult,
    normalize_input_text,
    normalize_input_texts,
    parse_embedding_response,
)


DEFAULT_EMBEDDING_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")


def get_embeddings_client() -> OpenAI:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required")
    base_url = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
    return OpenAI(api_key=api_key, base_url=base_url)


def create_embedding(
    text: str, model: str = DEFAULT_EMBEDDING_MODEL
) -> EmbeddingResult:
    client = get_embeddings_client()
    response = client.embeddings.create(model=model, input=normalize_input_text(text))
    return parse_embedding_response(response.model_dump())


def create_embeddings(
    texts: Sequence[str], model: str = DEFAULT_EMBEDDING_MODEL
) -> EmbeddingResult:
    normalized_texts = normalize_input_texts(texts)
    client = get_embeddings_client()
    response = client.embeddings.create(model=model, input=normalized_texts)
    return parse_embedding_response(response.model_dump())
