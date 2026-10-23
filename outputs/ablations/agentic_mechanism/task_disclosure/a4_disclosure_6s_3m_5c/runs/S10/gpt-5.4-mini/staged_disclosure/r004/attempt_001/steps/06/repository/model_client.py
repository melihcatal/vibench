import os
from dataclasses import dataclass
from functools import lru_cache
from typing import Any, Dict, Optional

from openai import OpenAI


DEFAULT_MODEL_FAMILY = os.getenv("MODEL_FAMILY", "gpt-5")
DEFAULT_MODEL_ID = os.getenv("OPENAI_MODEL", "openai/gpt-5.4-mini")


@dataclass(frozen=True)
class ModelClientConfig:
    api_key: Optional[str] = None
    base_url: Optional[str] = None
    organization: Optional[str] = None
    project: Optional[str] = None
    model_family: str = DEFAULT_MODEL_FAMILY
    model_id: str = DEFAULT_MODEL_ID


def load_config() -> ModelClientConfig:
    return ModelClientConfig(
        api_key=os.getenv("OPENAI_API_KEY"),
        base_url=os.getenv("OPENAI_BASE_URL"),
        organization=os.getenv("OPENAI_ORG_ID"),
        project=os.getenv("OPENAI_PROJECT_ID"),
        model_family=os.getenv("MODEL_FAMILY", DEFAULT_MODEL_FAMILY),
        model_id=os.getenv("OPENAI_MODEL", DEFAULT_MODEL_ID),
    )


def select_model(family: Optional[str] = None) -> str:
    family_value = (family or os.getenv("MODEL_FAMILY") or DEFAULT_MODEL_FAMILY).strip().lower()
    mapping = {
        "gpt-5": os.getenv("OPENAI_MODEL_GPT5", DEFAULT_MODEL_ID),
        "gpt-4.1": os.getenv("OPENAI_MODEL_GPT41", "openai/gpt-4.1"),
        "gpt-4o": os.getenv("OPENAI_MODEL_GPT4O", "openai/gpt-4o"),
    }
    return mapping.get(family_value, os.getenv("OPENAI_MODEL", DEFAULT_MODEL_ID))


@lru_cache(maxsize=1)
def get_client() -> OpenAI:
    config = load_config()
    kwargs: Dict[str, Any] = {}
    if config.api_key:
        kwargs["api_key"] = config.api_key
    if config.base_url:
        kwargs["base_url"] = config.base_url
    if config.organization:
        kwargs["organization"] = config.organization
    if config.project:
        kwargs["project"] = config.project
    return OpenAI(**kwargs)


def get_default_model() -> str:
    return select_model()


def chat_completion(
    messages: list,
    model: Optional[str] = None,
    **kwargs: Any,
):
    resolved_model = model or get_default_model()
    return get_client().chat.completions.create(model=resolved_model, messages=messages, **kwargs)
