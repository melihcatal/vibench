from __future__ import annotations

import os
from dataclasses import dataclass
from functools import lru_cache
from typing import Optional

from openai import OpenAI

DEFAULT_EMBEDDING_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")


@dataclass(frozen=True)
class EmbeddingsConfig:
    api_key: str
    model: str = DEFAULT_EMBEDDING_MODEL


def load_config() -> EmbeddingsConfig:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise EnvironmentError("OPENAI_API_KEY is required for OpenAI embeddings")
    return EmbeddingsConfig(api_key=api_key, model=DEFAULT_EMBEDDING_MODEL)


@lru_cache(maxsize=1)
def get_client(api_key: Optional[str] = None) -> OpenAI:
    key = api_key or os.environ.get("OPENAI_API_KEY")
    if not key:
        raise EnvironmentError("OPENAI_API_KEY is required for OpenAI embeddings")
    return OpenAI(api_key=key)


def get_model_name(model: Optional[str] = None) -> str:
    return model or DEFAULT_EMBEDDING_MODEL
