import os
from dataclasses import dataclass
from typing import Any, Dict, Optional

from openai import OpenAI


@dataclass
class ModelConfig:
    api_key: Optional[str] = None
    model: str = "gpt-4.1-mini"
    base_url: Optional[str] = None


def load_config() -> ModelConfig:
    return ModelConfig(
        api_key=os.getenv("OPENAI_API_KEY"),
        model=os.getenv("OPENAI_MODEL", "gpt-4.1-mini"),
        base_url=os.getenv("OPENAI_BASE_URL"),
    )


def get_client(config: Optional[ModelConfig] = None) -> OpenAI:
    cfg = config or load_config()
    kwargs: Dict[str, Any] = {"api_key": cfg.api_key}
    if cfg.base_url:
        kwargs["base_url"] = cfg.base_url
    return OpenAI(**kwargs)


def get_model_name(config: Optional[ModelConfig] = None) -> str:
    return (config or load_config()).model
