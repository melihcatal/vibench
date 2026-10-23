"""Client helpers for a direct embeddings API integration using OpenAI embeddings."""

from __future__ import annotations

import os
from functools import lru_cache
from typing import Optional

from openai import OpenAI

DEFAULT_EMBEDDING_MODEL = "text-embedding-3-small"


class EmbeddingsConfigError(RuntimeError):
    pass


@lru_cache(maxsize=1)
def get_openai_client() -> OpenAI:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise EmbeddingsConfigError("OPENAI_API_KEY is required for OpenAI embeddings.")
    base_url = os.getenv("OPENAI_BASE_URL")
    if base_url:
        return OpenAI(api_key=api_key, base_url=base_url)
    return OpenAI(api_key=api_key)


def get_embedding_model(default: Optional[str] = None) -> str:
    return os.getenv("OPENAI_EMBEDDING_MODEL", default or DEFAULT_EMBEDDING_MODEL)
