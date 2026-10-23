import os
from dataclasses import dataclass
from typing import Optional

from openai import OpenAI


@dataclass(frozen=True)
class LLMConfig:
    api_key: Optional[str]
    base_url: Optional[str]
    model: str
    response_format: Optional[str]


def load_config(default_model: str = "gpt-5.4-mini") -> LLMConfig:
    return LLMConfig(
        api_key=os.getenv("OPENAI_API_KEY"),
        base_url=os.getenv("OPENAI_BASE_URL"),
        model=os.getenv("OPENAI_MODEL", default_model),
        response_format=os.getenv("OPENAI_RESPONSE_FORMAT"),
    )


def create_client() -> OpenAI:
    cfg = load_config()
    return OpenAI(api_key=cfg.api_key, base_url=cfg.base_url)


def model_name() -> str:
    return load_config().model
