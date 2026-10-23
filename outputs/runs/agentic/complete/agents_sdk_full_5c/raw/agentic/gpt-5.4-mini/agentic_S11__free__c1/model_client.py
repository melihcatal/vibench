from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Optional

from openai import OpenAI

DEFAULT_MODEL = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")
DEFAULT_EMBEDDING_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")
DEFAULT_TTS_MODEL = os.getenv("OPENAI_TTS_MODEL", "gpt-4o-mini-tts")
DEFAULT_SAFETY_MODEL = os.getenv("OPENAI_SAFETY_MODEL", "gpt-4.1-mini")
DEFAULT_TRANSLATION_MODEL = os.getenv("OPENAI_TRANSLATION_MODEL", "gpt-4.1-mini")


@dataclass(frozen=True)
class PlatformClientConfig:
    api_key: Optional[str] = None
    organization: Optional[str] = None
    project: Optional[str] = None
    base_url: Optional[str] = None


def load_config() -> PlatformClientConfig:
    return PlatformClientConfig(
        api_key=os.getenv("OPENAI_API_KEY"),
        organization=os.getenv("OPENAI_ORG_ID") or os.getenv("OPENAI_ORGANIZATION"),
        project=os.getenv("OPENAI_PROJECT_ID") or os.getenv("OPENAI_PROJECT"),
        base_url=os.getenv("OPENAI_BASE_URL"),
    )


def get_client() -> OpenAI:
    cfg = load_config()
    kwargs = {}
    if cfg.api_key:
        kwargs["api_key"] = cfg.api_key
    if cfg.organization:
        kwargs["organization"] = cfg.organization
    if cfg.project:
        kwargs["project"] = cfg.project
    if cfg.base_url:
        kwargs["base_url"] = cfg.base_url
    return OpenAI(**kwargs)
