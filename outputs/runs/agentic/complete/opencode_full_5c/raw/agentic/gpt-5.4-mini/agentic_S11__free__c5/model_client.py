import os
from dataclasses import dataclass

from openai import OpenAI


@dataclass
class PlatformConfig:
    api_key: str
    project: str | None
    base_url: str | None
    model: str


def load_platform_config() -> PlatformConfig:
    return PlatformConfig(
        api_key=os.environ.get("OPENAI_API_KEY", ""),
        project=os.environ.get("OPENAI_PROJECT"),
        base_url=os.environ.get("OPENAI_BASE_URL"),
        model=os.environ.get("OPENAI_MODEL", "gpt-4.1-mini"),
    )


def create_platform_client() -> OpenAI:
    config = load_platform_config()
    return OpenAI(
        api_key=config.api_key, project=config.project, base_url=config.base_url
    )
