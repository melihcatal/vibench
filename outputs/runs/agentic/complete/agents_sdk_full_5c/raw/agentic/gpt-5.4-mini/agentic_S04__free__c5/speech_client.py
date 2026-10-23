from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any, Dict, Optional

from openai import OpenAI


DEFAULT_TRANSCRIBE_MODEL = os.getenv("OPENAI_TRANSCRIBE_MODEL", "gpt-4o-transcribe")
DEFAULT_LANGUAGE_MODEL = os.getenv("OPENAI_LANGUAGE_MODEL", "gpt-4.1-mini")
DEFAULT_EMBEDDING_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-large")


@dataclass(frozen=True)
class SpeechServiceConfig:
    api_key: Optional[str] = None
    base_url: Optional[str] = None
    transcribe_model: str = DEFAULT_TRANSCRIBE_MODEL
    language_model: str = DEFAULT_LANGUAGE_MODEL
    embedding_model: str = DEFAULT_EMBEDDING_MODEL

    @classmethod
    def from_env(cls) -> "SpeechServiceConfig":
        return cls(
            api_key=os.getenv("OPENAI_API_KEY"),
            base_url=os.getenv("OPENAI_BASE_URL"),
            transcribe_model=os.getenv("OPENAI_TRANSCRIBE_MODEL", DEFAULT_TRANSCRIBE_MODEL),
            language_model=os.getenv("OPENAI_LANGUAGE_MODEL", DEFAULT_LANGUAGE_MODEL),
            embedding_model=os.getenv("OPENAI_EMBEDDING_MODEL", DEFAULT_EMBEDDING_MODEL),
        )


def get_client(config: Optional[SpeechServiceConfig] = None) -> OpenAI:
    cfg = config or SpeechServiceConfig.from_env()
    kwargs: Dict[str, Any] = {}
    if cfg.api_key:
        kwargs["api_key"] = cfg.api_key
    if cfg.base_url:
        kwargs["base_url"] = cfg.base_url
    return OpenAI(**kwargs)
