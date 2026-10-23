import os
from dataclasses import dataclass
from typing import Any, Dict, Optional

from openai import OpenAI


DEFAULT_MODEL_FAMILY = "gpt-5"
DEFAULT_MODEL_ID = "openai/gpt-5.4-mini"


@dataclass(frozen=True)
class ModelConfig:
    api_key: Optional[str] = None
    base_url: Optional[str] = None
    model_family: str = DEFAULT_MODEL_FAMILY
    model_id: str = DEFAULT_MODEL_ID


def load_model_config() -> ModelConfig:
    return ModelConfig(
        api_key=os.getenv("OPENAI_API_KEY"),
        base_url=os.getenv("OPENAI_BASE_URL"),
        model_family=os.getenv("MODEL_FAMILY", DEFAULT_MODEL_FAMILY),
        model_id=os.getenv("MODEL_ID", DEFAULT_MODEL_ID),
    )


def resolve_model_id(model_family: Optional[str] = None, model_id: Optional[str] = None) -> str:
    if model_id:
        return model_id
    family = (model_family or os.getenv("MODEL_FAMILY") or DEFAULT_MODEL_FAMILY).strip().lower()
    if family in {"gpt-5", "gpt5"}:
        return os.getenv("MODEL_ID", DEFAULT_MODEL_ID)
    if family in {"gpt-4.1", "gpt4.1", "gpt-4", "gpt4"}:
        return os.getenv("MODEL_ID", "openai/gpt-4.1")
    return os.getenv("MODEL_ID", DEFAULT_MODEL_ID)


def build_client(config: Optional[ModelConfig] = None) -> OpenAI:
    cfg = config or load_model_config()
    kwargs: Dict[str, Any] = {}
    if cfg.api_key:
        kwargs["api_key"] = cfg.api_key
    if cfg.base_url:
        kwargs["base_url"] = cfg.base_url
    return OpenAI(**kwargs)


def complete_chat(
    messages: Any,
    *,
    model_family: Optional[str] = None,
    model_id: Optional[str] = None,
    temperature: float = 0.2,
    max_output_tokens: Optional[int] = None,
    config: Optional[ModelConfig] = None,
    **kwargs: Any,
) -> Any:
    cfg = config or load_model_config()
    client = build_client(cfg)
    resolved_model = resolve_model_id(model_family=model_family or cfg.model_family, model_id=model_id or cfg.model_id)
    payload: Dict[str, Any] = {
        "model": resolved_model,
        "messages": messages,
        "temperature": temperature,
        **kwargs,
    }
    if max_output_tokens is not None:
        payload["max_output_tokens"] = max_output_tokens
    return client.chat.completions.create(**payload)


def get_default_model_family() -> str:
    return os.getenv("MODEL_FAMILY", DEFAULT_MODEL_FAMILY)


def get_default_model_id() -> str:
    return resolve_model_id()
