from __future__ import annotations

import os
from dataclasses import dataclass
from functools import lru_cache
from typing import Optional

from openai import OpenAI

DEFAULT_EMBEDDING_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")
DEFAULT_CHAT_MODEL = os.getenv("OPENAI_CHAT_MODEL", "gpt-4o-mini")


@dataclass(frozen=True)
class EmbeddingsConfig:
    api_key: str
    embedding_model: str = DEFAULT_EMBEDDING_MODEL
    chat_model: str = DEFAULT_CHAT_MODEL


def load_embeddings_config() -> EmbeddingsConfig:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required for OpenAI embeddings integrations")
    return EmbeddingsConfig(api_key=api_key)


@lru_cache(maxsize=1)
def get_openai_client() -> OpenAI:
    cfg = load_embeddings_config()
    return OpenAI(api_key=cfg.api_key)


def get_embedding_model() -> str:
    return load_embeddings_config().embedding_model


def get_chat_model() -> str:
    return load_embeddings_config().chat_model


def client_or_none() -> Optional[OpenAI]:
    try:
        return get_openai_client()
    except RuntimeError:
        return None
