import json
import os
from dataclasses import dataclass
from typing import Any, Dict, Optional

import openai


DEFAULT_MODEL_FAMILY = "openai"
DEFAULT_MODEL = "openai/gpt-5.4-mini"


@dataclass(frozen=True)
class ModelConfig:
    provider: str = DEFAULT_MODEL_FAMILY
    model: str = DEFAULT_MODEL
    api_key: Optional[str] = None
    base_url: Optional[str] = None


def load_model_config() -> ModelConfig:
    provider = os.getenv("MODEL_PROVIDER", DEFAULT_MODEL_FAMILY).strip() or DEFAULT_MODEL_FAMILY
    model = os.getenv("MODEL_ID", DEFAULT_MODEL).strip() or DEFAULT_MODEL
    api_key = os.getenv("OPENAI_API_KEY")
    base_url = os.getenv("OPENAI_BASE_URL") or os.getenv("OPENAI_API_BASE")
    return ModelConfig(provider=provider, model=model, api_key=api_key, base_url=base_url)


def resolve_model_family(model: Optional[str] = None) -> str:
    value = (model or load_model_config().model).strip().lower()
    if value.startswith("openai/"):
        return "openai"
    if value.startswith("gpt-"):
        return "openai"
    if value.startswith("anthropic/"):
        return "anthropic"
    if value.startswith("claude-"):
        return "anthropic"
    if value.startswith("gemini/"):
        return "google"
    if value.startswith("google/"):
        return "google"
    return load_model_config().provider


def build_openai_client(config: Optional[ModelConfig] = None) -> openai.OpenAI:
    cfg = config or load_model_config()
    kwargs: Dict[str, Any] = {}
    if cfg.api_key:
        kwargs["api_key"] = cfg.api_key
    if cfg.base_url:
        kwargs["base_url"] = cfg.base_url
    return openai.OpenAI(**kwargs)


def get_client(config: Optional[ModelConfig] = None) -> Any:
    cfg = config or load_model_config()
    family = resolve_model_family(cfg.model)
    if family == "openai":
        return build_openai_client(cfg)
    raise ValueError(f"Unsupported model family: {family}")


def chat_completion(
    messages: list[Dict[str, str]],
    model: Optional[str] = None,
    temperature: float = 0.0,
    **kwargs: Any,
) -> str:
    cfg = load_model_config()
    selected_model = model or cfg.model
    client = get_client(ModelConfig(provider=cfg.provider, model=selected_model, api_key=cfg.api_key, base_url=cfg.base_url))
    response = client.chat.completions.create(model=selected_model, messages=messages, temperature=temperature, **kwargs)
    return response.choices[0].message.content or ""


def config_as_dict() -> Dict[str, Any]:
    cfg = load_model_config()
    return {
        "provider": cfg.provider,
        "model": cfg.model,
        "family": resolve_model_family(cfg.model),
        "has_api_key": bool(cfg.api_key),
        "base_url": cfg.base_url,
    }


def config_json() -> str:
    return json.dumps(config_as_dict(), ensure_ascii=False, sort_keys=True)
