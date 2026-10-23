from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Iterable, Optional

from openai import OpenAI

DEFAULT_CHAT_MODEL = os.getenv("OPENAI_CHAT_MODEL", "gpt-4o-mini")
DEFAULT_EMBEDDING_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")
DEFAULT_TTS_MODEL = os.getenv("OPENAI_TTS_MODEL", "gpt-4o-mini-tts")


@dataclass(frozen=True)
class ClientConfig:
    api_key: str = os.getenv("OPENAI_API_KEY", "")
    base_url: Optional[str] = os.getenv("OPENAI_BASE_URL")
    organization: Optional[str] = os.getenv("OPENAI_ORG_ID")


def get_openai_client(config: Optional[ClientConfig] = None) -> OpenAI:
    cfg = config or ClientConfig()
    kwargs = {}
    if cfg.api_key:
        kwargs["api_key"] = cfg.api_key
    if cfg.base_url:
        kwargs["base_url"] = cfg.base_url
    if cfg.organization:
        kwargs["organization"] = cfg.organization
    return OpenAI(**kwargs)


def choose_model(preferred: Optional[str], family: str = "chat") -> str:
    if preferred:
        return preferred
    if family == "embedding":
        return DEFAULT_EMBEDDING_MODEL
    if family == "tts":
        return DEFAULT_TTS_MODEL
    return DEFAULT_CHAT_MODEL


def normalize_messages(system: Optional[str], user: str, extra: Optional[Iterable[dict]] = None) -> list[dict]:
    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    if extra:
        messages.extend(list(extra))
    messages.append({"role": "user", "content": user})
    return messages
