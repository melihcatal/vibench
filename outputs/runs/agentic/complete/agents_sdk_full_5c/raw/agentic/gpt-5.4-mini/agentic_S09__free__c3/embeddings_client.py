"""Client helpers for a direct embeddings API using OpenAI's hosted API."""
from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Optional

from openai import OpenAI

DEFAULT_EMBEDDING_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")
DEFAULT_CHAT_MODEL = os.getenv("OPENAI_CHAT_MODEL", "gpt-4o-mini")


@dataclass(frozen=True)
class APISettings:
    api_key: Optional[str] = None
    base_url: Optional[str] = None
    embedding_model: str = DEFAULT_EMBEDDING_MODEL
    chat_model: str = DEFAULT_CHAT_MODEL


def load_settings() -> APISettings:
    return APISettings(
        api_key=os.getenv("OPENAI_API_KEY"),
        base_url=os.getenv("OPENAI_BASE_URL"),
        embedding_model=os.getenv("OPENAI_EMBEDDING_MODEL", DEFAULT_EMBEDDING_MODEL),
        chat_model=os.getenv("OPENAI_CHAT_MODEL", DEFAULT_CHAT_MODEL),
    )


def get_client(settings: Optional[APISettings] = None) -> OpenAI:
    cfg = settings or load_settings()
    kwargs = {}
    if cfg.api_key:
        kwargs["api_key"] = cfg.api_key
    if cfg.base_url:
        kwargs["base_url"] = cfg.base_url
    return OpenAI(**kwargs)
