import os
from functools import lru_cache

from openai import OpenAI


def api_key() -> str:
    return os.getenv("OPENAI_API_KEY", "")


@lru_cache(maxsize=1)
def client() -> OpenAI:
    return OpenAI(api_key=api_key() or None)


def speech_model() -> str:
    return os.getenv("OPENAI_TTS_MODEL", "gpt-4o-mini-tts")


def transcription_model() -> str:
    return os.getenv("OPENAI_TRANSCRIBE_MODEL", "gpt-4o-mini-transcribe")


def translation_model() -> str:
    return os.getenv("OPENAI_TRANSLATE_MODEL", "gpt-4o-mini-transcribe")


def embedding_model() -> str:
    return os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")
