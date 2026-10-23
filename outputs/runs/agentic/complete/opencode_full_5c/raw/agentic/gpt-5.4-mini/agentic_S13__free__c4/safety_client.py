import os
from dataclasses import dataclass
from typing import Any, Dict, Optional

import openai


@dataclass
class SafetyClientConfig:
    api_key: Optional[str] = None
    base_url: Optional[str] = None


def load_config() -> SafetyClientConfig:
    return SafetyClientConfig(
        api_key=os.getenv("OPENAI_API_KEY"), base_url=os.getenv("OPENAI_BASE_URL")
    )


def get_client() -> openai.OpenAI:
    cfg = load_config()
    kwargs: Dict[str, Any] = {}
    if cfg.api_key:
        kwargs["api_key"] = cfg.api_key
    if cfg.base_url:
        kwargs["base_url"] = cfg.base_url
    return openai.OpenAI(**kwargs)


def model_name(default: str) -> str:
    return os.getenv("OPENAI_MODEL", default)
