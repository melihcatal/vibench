import os
from dataclasses import dataclass
from functools import lru_cache
from typing import Optional

import cohere


@dataclass(frozen=True)
class EmbeddingsConfig:
    api_key: str
    model: str = "embed-english-v3.0"
    input_type: str = "search_document"
    embedding_types: tuple[str, ...] = ("float",)


@lru_cache(maxsize=1)
def load_config() -> EmbeddingsConfig:
    return EmbeddingsConfig(
        api_key=os.environ.get("COHERE_API_KEY", ""),
        model=os.environ.get("COHERE_EMBED_MODEL", "embed-english-v3.0"),
        input_type=os.environ.get("COHERE_EMBED_INPUT_TYPE", "search_document"),
    )


@lru_cache(maxsize=1)
def get_client() -> cohere.Client:
    cfg = load_config()
    if not cfg.api_key:
        raise RuntimeError("COHERE_API_KEY is required for Cohere Embed API")
    return cohere.Client(cfg.api_key)


def get_model() -> str:
    return load_config().model


def normalize_text(text: str) -> str:
    return " ".join(text.strip().split())


def resolve_input_type(task: Optional[str] = None) -> str:
    if task:
        return task
    return load_config().input_type
