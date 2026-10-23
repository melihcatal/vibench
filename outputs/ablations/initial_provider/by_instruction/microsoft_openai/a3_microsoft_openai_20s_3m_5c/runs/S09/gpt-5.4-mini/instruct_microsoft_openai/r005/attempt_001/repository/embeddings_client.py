import os
from dataclasses import dataclass
from functools import lru_cache
from typing import Optional

from openai import OpenAI


@dataclass(frozen=True)
class EmbeddingConfig:
    api_key: Optional[str]
    base_url: Optional[str]
    model: str


def load_config(default_model: str = "text-embedding-3-large") -> EmbeddingConfig:
    return EmbeddingConfig(
        api_key=os.getenv("OPENAI_API_KEY") or os.getenv("AZURE_OPENAI_API_KEY"),
        base_url=os.getenv("OPENAI_BASE_URL") or os.getenv("AZURE_OPENAI_ENDPOINT"),
        model=os.getenv("OPENAI_EMBEDDING_MODEL") or os.getenv("AZURE_OPENAI_EMBEDDING_MODEL") or default_model,
    )


@lru_cache(maxsize=4)
def get_client(api_key: Optional[str] = None, base_url: Optional[str] = None) -> OpenAI:
    kwargs = {}
    if api_key:
        kwargs["api_key"] = api_key
    if base_url:
        kwargs["base_url"] = base_url
    return OpenAI(**kwargs)


def get_embedding_client(default_model: str = "text-embedding-3-large"):
    config = load_config(default_model=default_model)
    client = get_client(config.api_key, config.base_url)
    return client, config
