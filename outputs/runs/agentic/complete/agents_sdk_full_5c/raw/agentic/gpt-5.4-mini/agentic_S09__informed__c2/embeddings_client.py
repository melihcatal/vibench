import os
from dataclasses import dataclass
from functools import lru_cache
from typing import Optional

from openai import OpenAI


@dataclass(frozen=True)
class EmbeddingsConfig:
    api_key: Optional[str]
    model: str = "text-embedding-3-small"
    base_url: Optional[str] = None


def load_config() -> EmbeddingsConfig:
    return EmbeddingsConfig(
        api_key=os.getenv("OPENAI_API_KEY"),
        model=os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small"),
        base_url=os.getenv("OPENAI_BASE_URL"),
    )


@lru_cache(maxsize=1)
def get_client() -> OpenAI:
    cfg = load_config()
    kwargs = {}
    if cfg.api_key:
        kwargs["api_key"] = cfg.api_key
    if cfg.base_url:
        kwargs["base_url"] = cfg.base_url
    return OpenAI(**kwargs)


def embedding_model() -> str:
    return load_config().model
