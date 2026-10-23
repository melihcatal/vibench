import os
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from openai import OpenAI


@dataclass
class EmbeddingsConfig:
    api_key: Optional[str] = None
    model: str = "text-embedding-3-small"
    dimensions: Optional[int] = None
    base_url: Optional[str] = None


def load_config() -> EmbeddingsConfig:
    return EmbeddingsConfig(
        api_key=os.getenv("OPENAI_API_KEY"),
        model=os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small"),
        dimensions=_optional_int(os.getenv("OPENAI_EMBEDDING_DIMENSIONS")),
        base_url=os.getenv("OPENAI_BASE_URL"),
    )


def create_client(config: Optional[EmbeddingsConfig] = None) -> OpenAI:
    cfg = config or load_config()
    kwargs: Dict[str, Any] = {}
    if cfg.api_key:
        kwargs["api_key"] = cfg.api_key
    if cfg.base_url:
        kwargs["base_url"] = cfg.base_url
    return OpenAI(**kwargs)


def embedding_request_kwargs(
    config: Optional[EmbeddingsConfig] = None,
) -> Dict[str, Any]:
    cfg = config or load_config()
    payload: Dict[str, Any] = {"model": cfg.model}
    if cfg.dimensions is not None:
        payload["dimensions"] = cfg.dimensions
    return payload


def _optional_int(value: Optional[str]) -> Optional[int]:
    if value is None or value == "":
        return None
    return int(value)


def extract_vectors(response: Any) -> List[List[float]]:
    return [list(item.embedding) for item in response.data]
