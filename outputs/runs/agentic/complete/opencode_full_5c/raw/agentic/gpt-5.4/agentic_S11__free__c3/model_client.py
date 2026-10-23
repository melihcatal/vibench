import os
from typing import Optional

from openai import OpenAI


DEFAULT_MODEL = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")
DEFAULT_EMBEDDING_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")
DEFAULT_AUDIO_MODEL = os.getenv("OPENAI_AUDIO_MODEL", "gpt-4o-mini-tts")
DEFAULT_VOICE = os.getenv("OPENAI_VOICE", "alloy")


def get_client(api_key: Optional[str] = None, base_url: Optional[str] = None) -> OpenAI:
    return OpenAI(
        api_key=api_key or os.getenv("OPENAI_API_KEY"),
        base_url=base_url or os.getenv("OPENAI_BASE_URL"),
    )


def resolve_model(model: Optional[str] = None) -> str:
    return model or DEFAULT_MODEL


def resolve_embedding_model(model: Optional[str] = None) -> str:
    return model or DEFAULT_EMBEDDING_MODEL


def resolve_audio_model(model: Optional[str] = None) -> str:
    return model or DEFAULT_AUDIO_MODEL


def resolve_voice(voice: Optional[str] = None) -> str:
    return voice or DEFAULT_VOICE
