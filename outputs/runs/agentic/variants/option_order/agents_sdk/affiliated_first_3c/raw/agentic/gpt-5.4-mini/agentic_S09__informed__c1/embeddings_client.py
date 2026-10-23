import os
from dataclasses import dataclass
from functools import lru_cache
from typing import Optional

from openai import OpenAI


@dataclass(frozen=True)
class EmbeddingClientConfig:
    api_key: str
    model: str = "text-embedding-3-small"
    base_url: Optional[str] = None


@lru_cache(maxsize=1)
def load_config() -> EmbeddingClientConfig:
    api_key = os.getenv("OPENAI_API_KEY", "")
    if not api_key:
        raise ValueError("OPENAI_API_KEY is required for OpenAI Embeddings")
    return EmbeddingClientConfig(
        api_key=api_key,
        model=os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small"),
        base_url=os.getenv("OPENAI_BASE_URL"),
    )


@lru_cache(maxsize=1)
def get_openai_client() -> OpenAI:
    cfg = load_config()
    kwargs = {"api_key": cfg.api_key}
    if cfg.base_url:
        kwargs["base_url"] = cfg.base_url
    return OpenAI(**kwargs)
