import os
from dataclasses import dataclass
from typing import Optional

from openai import OpenAI


@dataclass(frozen=True)
class SpeechClientConfig:
    api_key: Optional[str] = None
    organization: Optional[str] = None
    project: Optional[str] = None
    base_url: Optional[str] = None


def load_config() -> SpeechClientConfig:
    return SpeechClientConfig(
        api_key=os.getenv("OPENAI_API_KEY"),
        organization=os.getenv("OPENAI_ORG_ID"),
        project=os.getenv("OPENAI_PROJECT_ID"),
        base_url=os.getenv("OPENAI_BASE_URL"),
    )


def get_client(config: Optional[SpeechClientConfig] = None) -> OpenAI:
    cfg = config or load_config()
    kwargs = {"api_key": cfg.api_key}
    if cfg.organization:
        kwargs["organization"] = cfg.organization
    if cfg.project:
        kwargs["project"] = cfg.project
    if cfg.base_url:
        kwargs["base_url"] = cfg.base_url
    return OpenAI(**kwargs)
