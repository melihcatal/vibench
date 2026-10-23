import os
from functools import lru_cache
from typing import Optional

from openai import OpenAI

OPENAI_API_KEY_ENV = "OPENAI_API_KEY"
OPENAI_BASE_URL_ENV = "OPENAI_BASE_URL"
TEXT_MODEL_ENV = "OPENAI_TEXT_MODEL"
REASONING_MODEL_ENV = "OPENAI_REASONING_MODEL"
STRUCTURED_MODEL_ENV = "OPENAI_STRUCTURED_MODEL"
SAFETY_MODEL_ENV = "OPENAI_SAFETY_MODEL"
TRANSLATION_MODEL_ENV = "OPENAI_TRANSLATION_MODEL"
EMBEDDING_MODEL_ENV = "OPENAI_EMBEDDING_MODEL"
AUDIO_MODEL_ENV = "OPENAI_AUDIO_MODEL"


@lru_cache(maxsize=1)
def get_client() -> OpenAI:
    kwargs = {}
    base_url = os.getenv(OPENAI_BASE_URL_ENV)
    if base_url:
        kwargs["base_url"] = base_url
    return OpenAI(**kwargs)


def _select_model(env_name: str, default: str) -> str:
    return os.getenv(env_name, default)


def select_text_model(default: str = "gpt-4o-mini") -> str:
    return _select_model(TEXT_MODEL_ENV, default)


def select_reasoning_model(default: str = "gpt-4o-mini") -> str:
    return _select_model(REASONING_MODEL_ENV, default)


def select_structured_model(default: str = "gpt-4o-mini") -> str:
    return _select_model(STRUCTURED_MODEL_ENV, default)


def select_safety_model(default: str = "gpt-4o-mini") -> str:
    return _select_model(SAFETY_MODEL_ENV, default)


def select_translation_model(default: str = "gpt-4o-mini") -> str:
    return _select_model(TRANSLATION_MODEL_ENV, default)


def select_embedding_model(default: str = "text-embedding-3-small") -> str:
    return _select_model(EMBEDDING_MODEL_ENV, default)


def select_audio_model(default: str = "gpt-4o-mini-tts") -> str:
    return _select_model(AUDIO_MODEL_ENV, default)
