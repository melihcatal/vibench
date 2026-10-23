import os
from dataclasses import dataclass
from functools import lru_cache
from typing import Any, Dict, List, Optional

from openai import OpenAI

DEFAULT_EMBEDDING_MODEL = os.getenv('OPENAI_EMBEDDING_MODEL', 'text-embedding-3-small')

@dataclass(frozen=True)
class EmbeddingConfig:
    api_key: Optional[str]
    model: str
    base_url: Optional[str] = None


def load_config() -> EmbeddingConfig:
    return EmbeddingConfig(
        api_key=os.getenv('OPENAI_API_KEY'),
        model=DEFAULT_EMBEDDING_MODEL,
        base_url=os.getenv('OPENAI_BASE_URL'),
    )


@lru_cache(maxsize=1)
def get_client() -> OpenAI:
    config = load_config()
    kwargs: Dict[str, Any] = {}
    if config.api_key:
        kwargs['api_key'] = config.api_key
    if config.base_url:
        kwargs['base_url'] = config.base_url
    return OpenAI(**kwargs)


def get_embedding_model() -> str:
    return load_config().model


def ensure_texts(texts: List[str]) -> List[str]:
    return [str(text) for text in texts]
