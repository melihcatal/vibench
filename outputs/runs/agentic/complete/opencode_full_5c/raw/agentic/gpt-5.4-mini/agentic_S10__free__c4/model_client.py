import os
from dataclasses import dataclass
from typing import Any, Dict, Iterator, Optional

from openai import OpenAI


DEFAULT_MODEL = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")


@dataclass
class ModelClientConfig:
    api_key: Optional[str] = None
    base_url: Optional[str] = None
    model: str = DEFAULT_MODEL


def load_config(model: Optional[str] = None) -> ModelClientConfig:
    return ModelClientConfig(
        api_key=os.getenv("OPENAI_API_KEY"),
        base_url=os.getenv("OPENAI_BASE_URL"),
        model=model or DEFAULT_MODEL,
    )


def get_client(config: Optional[ModelClientConfig] = None) -> OpenAI:
    cfg = config or load_config()
    kwargs: Dict[str, Any] = {}
    if cfg.api_key:
        kwargs["api_key"] = cfg.api_key
    if cfg.base_url:
        kwargs["base_url"] = cfg.base_url
    return OpenAI(**kwargs)


def get_model(config: Optional[ModelClientConfig] = None) -> str:
    return (config or load_config()).model


def stream_text(response: Any) -> Iterator[str]:
    for event in response:
        delta = getattr(event.choices[0].delta, "content", None)
        if delta:
            yield delta
