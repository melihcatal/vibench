from __future__ import annotations

import os
from dataclasses import dataclass
from functools import lru_cache
from typing import Optional

from openai import OpenAI


@dataclass(frozen=True)
class TranslationClientConfig:
    api_key: Optional[str] = None
    base_url: Optional[str] = None
    organization: Optional[str] = None
    project: Optional[str] = None
    model: str = "gpt-5.4-mini"


def load_translation_client_config() -> TranslationClientConfig:
    return TranslationClientConfig(
        api_key=os.getenv("OPENAI_API_KEY"),
        base_url=os.getenv("OPENAI_BASE_URL"),
        organization=os.getenv("OPENAI_ORG_ID"),
        project=os.getenv("OPENAI_PROJECT_ID"),
        model=os.getenv("TRANSLATION_MODEL", "gpt-5.4-mini"),
    )


@lru_cache(maxsize=1)
def get_translation_client() -> OpenAI:
    config = load_translation_client_config()
    kwargs = {}
    if config.api_key:
        kwargs["api_key"] = config.api_key
    if config.base_url:
        kwargs["base_url"] = config.base_url
    if config.organization:
        kwargs["organization"] = config.organization
    if config.project:
        kwargs["project"] = config.project
    return OpenAI(**kwargs)


def get_translation_model() -> str:
    return load_translation_client_config().model


def reset_translation_client_cache() -> None:
    get_translation_client.cache_clear()
