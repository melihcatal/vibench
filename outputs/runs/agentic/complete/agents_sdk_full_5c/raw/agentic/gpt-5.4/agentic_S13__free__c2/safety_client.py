from __future__ import annotations

import os
from typing import Optional

from openai import OpenAI

from safety_models import (
    DEFAULT_OPENAI_CHAT_MODEL,
    DEFAULT_OPENAI_EMBEDDING_MODEL,
    DEFAULT_OPENAI_MODERATION_MODEL,
    DEFAULT_OPENAI_TRANSLATION_MODEL,
    DEFAULT_OPENAI_TTS_MODEL,
)


def get_openai_api_key(explicit_api_key: Optional[str] = None) -> str:
    api_key = explicit_api_key or os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY is required")
    return api_key


def get_openai_client(api_key: Optional[str] = None) -> OpenAI:
    return OpenAI(api_key=get_openai_api_key(api_key))


def moderation_model(model: Optional[str] = None) -> str:
    return model or os.getenv("OPENAI_MODERATION_MODEL", DEFAULT_OPENAI_MODERATION_MODEL)


def chat_model(model: Optional[str] = None) -> str:
    return model or os.getenv("OPENAI_CHAT_MODEL", DEFAULT_OPENAI_CHAT_MODEL)


def translation_model(model: Optional[str] = None) -> str:
    return model or os.getenv("OPENAI_TRANSLATION_MODEL", DEFAULT_OPENAI_TRANSLATION_MODEL)


def embedding_model(model: Optional[str] = None) -> str:
    return model or os.getenv("OPENAI_EMBEDDING_MODEL", DEFAULT_OPENAI_EMBEDDING_MODEL)


def tts_model(model: Optional[str] = None) -> str:
    return model or os.getenv("OPENAI_TTS_MODEL", DEFAULT_OPENAI_TTS_MODEL)
