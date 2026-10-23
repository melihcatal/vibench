from __future__ import annotations

import os
from typing import Optional

from openai import OpenAI


DEFAULT_TTS_MODEL = "gpt-4o-mini-tts"
DEFAULT_TRANSLATION_MODEL = "gpt-4.1-mini"
DEFAULT_MODERATION_MODEL = "omni-moderation-latest"
DEFAULT_EMBEDDING_MODEL = "text-embedding-3-large"
DEFAULT_TRANSCRIPTION_MODEL = "gpt-4o-mini-transcribe"


def get_openai_api_key(explicit_api_key: Optional[str] = None) -> str:
    api_key = explicit_api_key or os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY is required")
    return api_key


def get_openai_client(api_key: Optional[str] = None) -> OpenAI:
    return OpenAI(api_key=get_openai_api_key(api_key))


def resolve_tts_model(model: Optional[str] = None) -> str:
    return model or os.getenv("OPENAI_TTS_MODEL") or DEFAULT_TTS_MODEL


def resolve_translation_model(model: Optional[str] = None) -> str:
    return model or os.getenv("OPENAI_TRANSLATION_MODEL") or DEFAULT_TRANSLATION_MODEL


def resolve_moderation_model(model: Optional[str] = None) -> str:
    return model or os.getenv("OPENAI_MODERATION_MODEL") or DEFAULT_MODERATION_MODEL


def resolve_embedding_model(model: Optional[str] = None) -> str:
    return model or os.getenv("OPENAI_EMBEDDING_MODEL") or DEFAULT_EMBEDDING_MODEL


def resolve_transcription_model(model: Optional[str] = None) -> str:
    return (
        model or os.getenv("OPENAI_TRANSCRIPTION_MODEL") or DEFAULT_TRANSCRIPTION_MODEL
    )
