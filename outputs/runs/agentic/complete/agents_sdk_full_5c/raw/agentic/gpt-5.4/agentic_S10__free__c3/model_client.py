from __future__ import annotations

import os
from typing import Optional

from openai import OpenAI

DEFAULT_CHAT_MODEL = os.getenv("OPENAI_CHAT_MODEL", "gpt-4o-mini")
DEFAULT_REASONING_MODEL = os.getenv("OPENAI_REASONING_MODEL", "gpt-4.1-mini")
DEFAULT_EMBED_MODEL = os.getenv("OPENAI_EMBED_MODEL", "text-embedding-3-large")
DEFAULT_TTS_MODEL = os.getenv("OPENAI_TTS_MODEL", "gpt-4o-mini-tts")
DEFAULT_MODERATION_MODEL = os.getenv("OPENAI_MODERATION_MODEL", "omni-moderation-latest")


def get_openai_client(api_key: Optional[str] = None) -> OpenAI:
    return OpenAI(
        api_key=api_key or os.getenv("OPENAI_API_KEY"),
        base_url=os.getenv("OPENAI_BASE_URL"),
    )


def pick_chat_model(task: str) -> str:
    task = task.lower().strip()
    if task in {"summary", "extract", "qa", "stream", "translate"}:
        return DEFAULT_CHAT_MODEL
    if task in {"safety"}:
        return DEFAULT_REASONING_MODEL
    return DEFAULT_CHAT_MODEL
