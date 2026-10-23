import os
from dataclasses import dataclass

from openai import OpenAI


@dataclass
class PlatformConfig:
    api_key: str
    model: str
    base_url: str | None = None


def load_platform_config() -> PlatformConfig:
    return PlatformConfig(
        api_key=os.environ.get("OPENAI_API_KEY", ""),
        model=os.environ.get("OPENAI_MODEL", "gpt-4.1-mini"),
        base_url=os.environ.get("OPENAI_BASE_URL"),
    )


def build_platform_client(config: PlatformConfig | None = None) -> OpenAI:
    cfg = config or load_platform_config()
    kwargs = {"api_key": cfg.api_key}
    if cfg.base_url:
        kwargs["base_url"] = cfg.base_url
    return OpenAI(**kwargs)
