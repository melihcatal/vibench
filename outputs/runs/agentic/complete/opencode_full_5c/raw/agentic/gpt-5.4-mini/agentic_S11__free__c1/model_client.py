import os
from dataclasses import dataclass

from openai import OpenAI


@dataclass
class PlatformConfig:
    api_key: str
    project: str | None
    base_url: str | None


def load_platform_config() -> PlatformConfig:
    return PlatformConfig(
        api_key=os.getenv("OPENAI_API_KEY", ""),
        project=os.getenv("OPENAI_PROJECT"),
        base_url=os.getenv("OPENAI_BASE_URL"),
    )


def build_platform_client() -> OpenAI:
    cfg = load_platform_config()
    kwargs = {"api_key": cfg.api_key}
    if cfg.project:
        kwargs["project"] = cfg.project
    if cfg.base_url:
        kwargs["base_url"] = cfg.base_url
    return OpenAI(**kwargs)
