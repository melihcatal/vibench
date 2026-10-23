import os
from dataclasses import dataclass
from typing import Any, Dict, Optional

from openai import OpenAI


@dataclass(frozen=True)
class ModelClientConfig:
    api_key: str
    base_url: str
    model: str


def load_config() -> ModelClientConfig:
    return ModelClientConfig(
        api_key=os.environ.get("OPENAI_API_KEY", ""),
        base_url=os.environ.get("OPENAI_BASE_URL", "https://api.openai.com/v1"),
        model=os.environ.get("OPENAI_MODEL", "gpt-4.1-mini"),
    )


def create_client(config: Optional[ModelClientConfig] = None) -> OpenAI:
    cfg = config or load_config()
    if not cfg.api_key:
        raise ValueError("OPENAI_API_KEY is required")
    return OpenAI(api_key=cfg.api_key, base_url=cfg.base_url)


def chat_completion(
    messages: Any,
    *,
    config: Optional[ModelClientConfig] = None,
    **kwargs: Any,
) -> Dict[str, Any]:
    cfg = config or load_config()
    client = create_client(cfg)
    response = client.chat.completions.create(model=cfg.model, messages=messages, **kwargs)
    return response.model_dump()


def structured_model_context(config: Optional[ModelClientConfig] = None) -> Dict[str, str]:
    cfg = config or load_config()
    return {"provider": "openai", "model": cfg.model, "base_url": cfg.base_url}
