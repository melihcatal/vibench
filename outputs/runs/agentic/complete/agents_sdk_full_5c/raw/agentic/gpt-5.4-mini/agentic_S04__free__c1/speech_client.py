from __future__ import annotations

import os
from dataclasses import dataclass
from functools import lru_cache
from typing import Any, Dict, Optional

from openai import OpenAI

OPENAI_TRANSCRIBE_MODEL = os.getenv("OPENAI_TRANSCRIBE_MODEL", "gpt-4o-mini-transcribe")
OPENAI_TRANSLATE_MODEL = os.getenv("OPENAI_TRANSLATE_MODEL", "gpt-4o-mini-transcribe")
OPENAI_MODERATION_MODEL = os.getenv("OPENAI_MODERATION_MODEL", "omni-moderation-latest")
OPENAI_EMBEDDING_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-large")
OPENAI_SUMMARY_MODEL = os.getenv("OPENAI_SUMMARY_MODEL", "gpt-4.1-mini")


@dataclass(frozen=True)
class SpeechServiceConfig:
    api_key: Optional[str] = None
    base_url: Optional[str] = None


@lru_cache(maxsize=1)
def load_config() -> SpeechServiceConfig:
    return SpeechServiceConfig(
        api_key=os.getenv("OPENAI_API_KEY"),
        base_url=os.getenv("OPENAI_BASE_URL"),
    )


@lru_cache(maxsize=1)
def get_client() -> OpenAI:
    cfg = load_config()
    kwargs: Dict[str, Any] = {}
    if cfg.api_key:
        kwargs["api_key"] = cfg.api_key
    if cfg.base_url:
        kwargs["base_url"] = cfg.base_url
    return OpenAI(**kwargs)


def ensure_audio_file(path: str) -> str:
    if not path:
        raise ValueError("audio file path is required")
    return path


def normalize_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value.strip()
    return str(value).strip()
