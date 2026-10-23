from __future__ import annotations

import os
from functools import lru_cache
from typing import Optional

from openai import OpenAI

DEFAULT_EMBEDDING_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")
DEFAULT_CHAT_MODEL = os.getenv("OPENAI_CHAT_MODEL", "gpt-4o-mini")


@lru_cache(maxsize=1)
def get_openai_client() -> OpenAI:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required for OpenAI integrations")
    return OpenAI(api_key=api_key)


def get_embedding_model() -> str:
    return DEFAULT_EMBEDDING_MODEL


def get_chat_model() -> str:
    return DEFAULT_CHAT_MODEL


def coerce_text(value: Optional[str]) -> str:
    return "" if value is None else str(value)
