from __future__ import annotations

import os
from dataclasses import dataclass
from functools import lru_cache
from typing import Iterable, Optional

from openai import OpenAI

DEFAULT_EMBEDDING_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")


@dataclass(frozen=True)
class EmbeddingsConfig:
    api_key: str
    model: str = DEFAULT_EMBEDDING_MODEL


@lru_cache(maxsize=1)
def load_config() -> EmbeddingsConfig:
    api_key = os.getenv("OPENAI_API_KEY", "").strip()
    if not api_key:
        raise EnvironmentError("OPENAI_API_KEY is required for OpenAI Embeddings")
    model = os.getenv("OPENAI_EMBEDDING_MODEL", DEFAULT_EMBEDDING_MODEL).strip()
    return EmbeddingsConfig(api_key=api_key, model=model)


@lru_cache(maxsize=1)
def get_client() -> OpenAI:
    cfg = load_config()
    return OpenAI(api_key=cfg.api_key)


def get_embedding_model() -> str:
    return load_config().model


def normalize_input(texts: Iterable[str]) -> list[str]:
    normalized: list[str] = []
    for text in texts:
        value = " ".join(str(text).split())
        if value:
            normalized.append(value)
    return normalized
