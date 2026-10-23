import os
from functools import lru_cache

from openai import OpenAI


def _env(name: str, default: str | None = None) -> str | None:
    value = os.getenv(name)
    return value if value not in (None, "") else default


@lru_cache(maxsize=1)
def get_client() -> OpenAI:
    return OpenAI(api_key=_env("OPENAI_API_KEY"), base_url=_env("OPENAI_BASE_URL"))


def embedding_model() -> str:
    return _env("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")


def tts_model() -> str:
    return _env("OPENAI_TTS_MODEL", "gpt-4o-mini-tts")


def translator_model() -> str:
    return _env("OPENAI_TRANSLATION_MODEL", "gpt-4.1-mini")


def moderation_model() -> str:
    return _env("OPENAI_MODERATION_MODEL", "omni-moderation-latest")
