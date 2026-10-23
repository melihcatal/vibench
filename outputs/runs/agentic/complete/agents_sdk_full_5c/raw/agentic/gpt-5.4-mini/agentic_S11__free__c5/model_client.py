import os
from dataclasses import dataclass
from typing import Optional

from openai import OpenAI


@dataclass(frozen=True)
class PlatformConfig:
    api_key: str
    model: str = "gpt-4.1-mini"
    base_url: Optional[str] = None


def load_platform_config() -> PlatformConfig:
    api_key = os.environ.get("OPENAI_API_KEY", "")
    if not api_key:
        raise ValueError("OPENAI_API_KEY is required for OpenAI platform integration")
    return PlatformConfig(
        api_key=api_key,
        model=os.environ.get("OPENAI_MODEL", "gpt-4.1-mini"),
        base_url=os.environ.get("OPENAI_BASE_URL"),
    )


def create_platform_client() -> OpenAI:
    config = load_platform_config()
    kwargs = {"api_key": config.api_key}
    if config.base_url:
        kwargs["base_url"] = config.base_url
    return OpenAI(**kwargs)
