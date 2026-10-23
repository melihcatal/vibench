import os
from functools import lru_cache

from openai import OpenAI


def _env(name, default=None):
    value = os.getenv(name)
    return value if value else default


@lru_cache(maxsize=1)
def get_client():
    return OpenAI(api_key=_env("OPENAI_API_KEY"), base_url=_env("OPENAI_BASE_URL"))


def speech_model():
    return _env("OPENAI_TTS_MODEL", "gpt-4o-mini-tts")


def transcription_model():
    return _env("OPENAI_TRANSCRIBE_MODEL", "whisper-1")


def translation_model():
    return _env("OPENAI_TRANSLATE_MODEL", "gpt-4.1-mini")


def embedding_model():
    return _env("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")


def moderation_model():
    return _env("OPENAI_MODERATION_MODEL", "omni-moderation-latest")
