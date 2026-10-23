import os
from dataclasses import dataclass
from typing import Optional

from openai import OpenAI


@dataclass(frozen=True)
class PlatformClientConfig:
    api_key: Optional[str] = None
    base_url: Optional[str] = None
    organization: Optional[str] = None
    project: Optional[str] = None
    model: Optional[str] = None


def load_platform_client_config() -> PlatformClientConfig:
    return PlatformClientConfig(
        api_key=os.getenv("OPENAI_API_KEY"),
        base_url=os.getenv("OPENAI_BASE_URL"),
        organization=os.getenv("OPENAI_ORG_ID") or os.getenv("OPENAI_ORGANIZATION"),
        project=os.getenv("OPENAI_PROJECT"),
        model=os.getenv("OPENAI_MODEL", "gpt-4.1-mini"),
    )


def create_platform_client(config: Optional[PlatformClientConfig] = None) -> OpenAI:
    cfg = config or load_platform_client_config()
    kwargs = {}
    if cfg.api_key:
        kwargs["api_key"] = cfg.api_key
    if cfg.base_url:
        kwargs["base_url"] = cfg.base_url
    if cfg.organization:
        kwargs["organization"] = cfg.organization
    if cfg.project:
        kwargs["project"] = cfg.project
    return OpenAI(**kwargs)


def resolve_platform_model(config: Optional[PlatformClientConfig] = None) -> str:
    cfg = config or load_platform_client_config()
    if not cfg.model:
        raise ValueError("OPENAI_MODEL must be set or a model must be provided in config")
    return cfg.model
