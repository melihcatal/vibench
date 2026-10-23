import os
from dataclasses import dataclass
from functools import lru_cache
from typing import Any, Dict, Optional

from openai import OpenAI


DEFAULT_MODEL_FAMILY = "gpt-4o-mini"


@dataclass(frozen=True)
class ModelClientConfig:
    api_key: Optional[str] = None
    base_url: Optional[str] = None
    model: Optional[str] = None
    family: Optional[str] = None


def _env(key: str) -> Optional[str]:
    value = os.environ.get(key)
    return value if value else None


def load_config() -> ModelClientConfig:
    return ModelClientConfig(
        api_key=_env("OPENAI_API_KEY"),
        base_url=_env("OPENAI_BASE_URL"),
        model=_env("OPENAI_MODEL"),
        family=_env("OPENAI_MODEL_FAMILY"),
    )


def resolve_model_name(model: Optional[str] = None, family: Optional[str] = None) -> str:
    config = load_config()
    if model:
        return model
    if config.model:
        return config.model
    if family:
        return family
    if config.family:
        return config.family
    return DEFAULT_MODEL_FAMILY


def create_client(config: Optional[ModelClientConfig] = None) -> OpenAI:
    cfg = config or load_config()
    kwargs: Dict[str, Any] = {}
    if cfg.api_key:
        kwargs["api_key"] = cfg.api_key
    if cfg.base_url:
        kwargs["base_url"] = cfg.base_url
    return OpenAI(**kwargs)


@lru_cache(maxsize=1)
def get_client() -> OpenAI:
    return create_client()


def client_kwargs(model: Optional[str] = None, family: Optional[str] = None) -> Dict[str, str]:
    resolved = resolve_model_name(model=model, family=family)
    return {"model": resolved}


def normalize_model_family(model: Optional[str] = None, family: Optional[str] = None) -> str:
    resolved = resolve_model_name(model=model, family=family)
    if resolved.startswith("gpt-4o"):
        return "gpt-4o"
    if resolved.startswith("gpt-4.1"):
        return "gpt-4.1"
    if resolved.startswith("gpt-3.5"):
        return "gpt-3.5"
    return resolved
