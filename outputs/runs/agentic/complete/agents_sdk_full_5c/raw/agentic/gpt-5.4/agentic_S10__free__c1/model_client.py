from __future__ import annotations

import os
from typing import Iterable, Optional

from openai import OpenAI

DEFAULT_CHAT_MODEL = os.getenv("OPENAI_CHAT_MODEL", "gpt-4.1-mini")
DEFAULT_EMBED_MODEL = os.getenv("OPENAI_EMBED_MODEL", "text-embedding-3-small")
DEFAULT_TTS_MODEL = os.getenv("OPENAI_TTS_MODEL", "gpt-4o-mini-tts")
DEFAULT_MODERATION_MODEL = os.getenv("OPENAI_MODERATION_MODEL", "omni-moderation-latest")
DEFAULT_TRANSLATION_MODEL = os.getenv("OPENAI_TRANSLATION_MODEL", "gpt-4.1-mini")


def get_openai_client(api_key: Optional[str] = None) -> OpenAI:
    return OpenAI(api_key=api_key or os.getenv("OPENAI_API_KEY"))


def coalesce_text(parts: Iterable[Optional[str]]) -> str:
    return "\n\n".join(part.strip() for part in parts if part and part.strip())


def choose_model(task: str) -> str:
    mapping = {
        "summary": DEFAULT_CHAT_MODEL,
        "extract": DEFAULT_CHAT_MODEL,
        "qa": DEFAULT_CHAT_MODEL,
        "stream": DEFAULT_CHAT_MODEL,
        "translate": DEFAULT_TRANSLATION_MODEL,
    }
    return mapping.get(task, DEFAULT_CHAT_MODEL)
