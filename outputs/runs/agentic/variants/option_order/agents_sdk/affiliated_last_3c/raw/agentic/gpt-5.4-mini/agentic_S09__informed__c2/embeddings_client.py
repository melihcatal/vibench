import os
from dataclasses import dataclass
from functools import lru_cache
from typing import Optional

from openai import OpenAI

DEFAULT_EMBEDDING_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")


@dataclass(frozen=True)
class EmbeddingsConfig:
    api_key: Optional[str] = None
    model: str = DEFAULT_EMBEDDING_MODEL


@lru_cache(maxsize=1)
def load_config() -> EmbeddingsConfig:
    return EmbeddingsConfig(api_key=os.getenv("OPENAI_API_KEY"), model=DEFAULT_EMBEDDING_MODEL)


@lru_cache(maxsize=1)
def get_client() -> OpenAI:
    cfg = load_config()
    return OpenAI(api_key=cfg.api_key)


def embedding_model() -> str:
    return load_config().model
