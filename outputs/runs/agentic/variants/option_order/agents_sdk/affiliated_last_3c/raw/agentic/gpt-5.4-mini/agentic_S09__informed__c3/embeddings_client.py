from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any, List, Optional

from openai import OpenAI

DEFAULT_EMBEDDING_MODEL = "text-embedding-3-small"


@dataclass(frozen=True)
class EmbeddingsConfig:
    api_key: str
    model: str = DEFAULT_EMBEDDING_MODEL


def load_config() -> EmbeddingsConfig:
    api_key = os.getenv("OPENAI_API_KEY", "")
    if not api_key:
        raise EnvironmentError("OPENAI_API_KEY is required for OpenAI embeddings")
    model = os.getenv("OPENAI_EMBEDDING_MODEL", DEFAULT_EMBEDDING_MODEL)
    return EmbeddingsConfig(api_key=api_key, model=model)


def get_client(api_key: Optional[str] = None) -> OpenAI:
    key = api_key or os.getenv("OPENAI_API_KEY", "")
    if not key:
        raise EnvironmentError("OPENAI_API_KEY is required for OpenAI embeddings")
    return OpenAI(api_key=key)


def embed_texts(texts: List[str], model: Optional[str] = None) -> List[List[float]]:
    cfg = load_config()
    client = get_client(cfg.api_key)
    response = client.embeddings.create(model=model or cfg.model, input=texts)
    return [list(item.embedding) for item in response.data]


def embed_text(text: str, model: Optional[str] = None) -> List[float]:
    return embed_texts([text], model=model)[0]


def cosine_similarity(vec_a: List[float], vec_b: List[float]) -> float:
    dot = sum(a * b for a, b in zip(vec_a, vec_b))
    norm_a = sum(a * a for a in vec_a) ** 0.5
    norm_b = sum(b * b for b in vec_b) ** 0.5
    if norm_a == 0.0 or norm_b == 0.0:
        return 0.0
    return dot / (norm_a * norm_b)
