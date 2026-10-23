import os
from functools import lru_cache

from openai import OpenAI, AzureOpenAI


def _env(name, default=None):
    value = os.getenv(name)
    return value if value not in (None, "") else default


@lru_cache(maxsize=1)
def get_openai_client():
    api_key = _env("OPENAI_API_KEY")
    if _env("AZURE_OPENAI_ENDPOINT") and _env("AZURE_OPENAI_API_KEY"):
        return AzureOpenAI(
            api_key=_env("AZURE_OPENAI_API_KEY"),
            azure_endpoint=_env("AZURE_OPENAI_ENDPOINT"),
            api_version=_env("AZURE_OPENAI_API_VERSION", "2024-10-21"),
        )
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY or Azure OpenAI credentials are required")
    return OpenAI(api_key=api_key)


def get_transcription_model():
    return _env("OPENAI_TRANSCRIPTION_MODEL", "gpt-4o-mini-transcribe")


def get_translation_model():
    return _env("OPENAI_TRANSLATION_MODEL", "gpt-4o-mini")


def get_moderation_model():
    return _env("OPENAI_MODERATION_MODEL", "omni-moderation-latest")


def get_embedding_model():
    return _env("OPENAI_EMBEDDING_MODEL", "text-embedding-3-large")


def open_audio(path):
    return open(path, "rb")
