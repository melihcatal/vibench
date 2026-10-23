from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Optional

from openai import OpenAI


DEFAULT_OPENAI_MODERATION_MODEL = os.getenv("OPENAI_MODERATION_MODEL", "omni-moderation-latest")
DEFAULT_OPENAI_CHAT_MODEL = os.getenv("OPENAI_CHAT_MODEL", "gpt-4.1-mini")
DEFAULT_OPENAI_EMBEDDING_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")
DEFAULT_OPENAI_TTS_MODEL = os.getenv("OPENAI_TTS_MODEL", "gpt-4o-mini-tts")
DEFAULT_OPENAI_TRANSLATION_MODEL = os.getenv("OPENAI_TRANSLATION_MODEL", "gpt-4.1-mini")


@dataclass(frozen=True)
class SafetyConfig:
    api_key: Optional[str] = None
    moderation_model: str = DEFAULT_OPENAI_MODERATION_MODEL
    chat_model: str = DEFAULT_OPENAI_CHAT_MODEL
    embedding_model: str = DEFAULT_OPENAI_EMBEDDING_MODEL
    tts_model: str = DEFAULT_OPENAI_TTS_MODEL
    translation_model: str = DEFAULT_OPENAI_TRANSLATION_MODEL


def get_client(api_key: Optional[str] = None) -> OpenAI:
    key = api_key or os.getenv("OPENAI_API_KEY")
    return OpenAI(api_key=key)


def get_config() -> SafetyConfig:
    return SafetyConfig(
        api_key=os.getenv("OPENAI_API_KEY"),
        moderation_model=os.getenv("OPENAI_MODERATION_MODEL", DEFAULT_OPENAI_MODERATION_MODEL),
        chat_model=os.getenv("OPENAI_CHAT_MODEL", DEFAULT_OPENAI_CHAT_MODEL),
        embedding_model=os.getenv("OPENAI_EMBEDDING_MODEL", DEFAULT_OPENAI_EMBEDDING_MODEL),
        tts_model=os.getenv("OPENAI_TTS_MODEL", DEFAULT_OPENAI_TTS_MODEL),
        translation_model=os.getenv("OPENAI_TRANSLATION_MODEL", DEFAULT_OPENAI_TRANSLATION_MODEL),
    )
