import os
from dataclasses import dataclass
from typing import Any, Optional

from openai import OpenAI


DEFAULT_EMBEDDING_MODEL = "text-embedding-3-small"


@dataclass(frozen=True)
class EmbeddingsConfig:
    api_key: Optional[str] = None
    base_url: Optional[str] = None
    organization: Optional[str] = None
    project: Optional[str] = None
    model: str = DEFAULT_EMBEDDING_MODEL


def load_config() -> EmbeddingsConfig:
    return EmbeddingsConfig(
        api_key=os.environ.get("OPENAI_API_KEY"),
        base_url=os.environ.get("OPENAI_BASE_URL"),
        organization=os.environ.get("OPENAI_ORG_ID"),
        project=os.environ.get("OPENAI_PROJECT_ID"),
        model=os.environ.get("OPENAI_EMBEDDING_MODEL", DEFAULT_EMBEDDING_MODEL),
    )


def create_client(config: Optional[EmbeddingsConfig] = None) -> OpenAI:
    cfg = config or load_config()
    kwargs: dict[str, Any] = {}
    if cfg.api_key:
        kwargs["api_key"] = cfg.api_key
    if cfg.base_url:
        kwargs["base_url"] = cfg.base_url
    if cfg.organization:
        kwargs["organization"] = cfg.organization
    if cfg.project:
        kwargs["project"] = cfg.project
    return OpenAI(**kwargs)


def get_embedding_model(config: Optional[EmbeddingsConfig] = None) -> str:
    return (config or load_config()).model
