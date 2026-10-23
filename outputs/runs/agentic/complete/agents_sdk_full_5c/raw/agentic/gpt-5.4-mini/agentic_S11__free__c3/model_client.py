import os
from dataclasses import dataclass
from typing import Optional

from openai import OpenAI


@dataclass(frozen=True)
class PlatformConfig:
    api_key: str
    model: str = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")
    base_url: Optional[str] = None


def load_config() -> PlatformConfig:
    api_key = os.getenv("OPENAI_API_KEY", "").strip()
    if not api_key:
        raise ValueError("OPENAI_API_KEY is required")
    base_url = os.getenv("OPENAI_BASE_URL")
    model = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")
    return PlatformConfig(api_key=api_key, model=model, base_url=base_url)


def build_client(config: Optional[PlatformConfig] = None) -> OpenAI:
    cfg = config or load_config()
    kwargs = {"api_key": cfg.api_key}
    if cfg.base_url:
        kwargs["base_url"] = cfg.base_url
    return OpenAI(**kwargs)
