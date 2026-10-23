import os
from dataclasses import dataclass
from typing import Any, Dict, Mapping, Optional

import openai


DEFAULT_MODEL_FAMILY = "openai"
DEFAULT_MODEL_ID = "openai/gpt-5.4-mini"


@dataclass(frozen=True)
class ModelClientConfig:
    api_key: str
    model_family: str = DEFAULT_MODEL_FAMILY
    model_id: str = DEFAULT_MODEL_ID
    base_url: Optional[str] = None


def load_config(env: Mapping[str, str] = os.environ) -> ModelClientConfig:
    api_key = env.get("OPENAI_API_KEY", "")
    if not api_key:
        raise ValueError("OPENAI_API_KEY is required")
    return ModelClientConfig(
        api_key=api_key,
        model_family=env.get("MODEL_FAMILY", DEFAULT_MODEL_FAMILY),
        model_id=env.get("MODEL_ID", DEFAULT_MODEL_ID),
        base_url=env.get("OPENAI_BASE_URL"),
    )


def select_model_family(model_id: str) -> str:
    normalized = (model_id or "").strip().lower()
    if normalized.startswith("openai/") or normalized.startswith("gpt-"):
        return "openai"
    return DEFAULT_MODEL_FAMILY


def get_client(config: Optional[ModelClientConfig] = None) -> Any:
    cfg = config or load_config()
    kwargs: Dict[str, Any] = {"api_key": cfg.api_key}
    if cfg.base_url:
        kwargs["base_url"] = cfg.base_url
    return openai.OpenAI(**kwargs)


def resolve_model_id(model_family: str, model_id: Optional[str] = None) -> str:
    if model_id:
        return model_id
    if model_family == "openai":
        return DEFAULT_MODEL_ID
    return DEFAULT_MODEL_ID


def build_request_payload(prompt: str, context: Optional[str] = None, **kwargs: Any) -> Dict[str, Any]:
    messages = []
    if context:
        messages.append({"role": "system", "content": context})
    messages.append({"role": "user", "content": prompt})
    payload: Dict[str, Any] = {
        "model": kwargs.pop("model", DEFAULT_MODEL_ID),
        "messages": messages,
    }
    payload.update(kwargs)
    return payload
