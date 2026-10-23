import os
from functools import lru_cache
from typing import Optional

from openai import OpenAI


DEFAULT_MODEL = "gpt-5.4-mini"
DEFAULT_EMBED_MODEL = "text-embedding-3-large"
DEFAULT_TTS_MODEL = "gpt-4o-mini-tts"


def get_model_name(kind: str = "chat") -> str:
    if kind == "embedding":
        return os.getenv("OPENAI_EMBED_MODEL", DEFAULT_EMBED_MODEL)
    if kind == "tts":
        return os.getenv("OPENAI_TTS_MODEL", DEFAULT_TTS_MODEL)
    return os.getenv("OPENAI_MODEL", DEFAULT_MODEL)


@lru_cache(maxsize=1)
def get_openai_client() -> OpenAI:
    return OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def build_messages(system: Optional[str], user: str, context: Optional[str] = None):
    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    if context:
        messages.append({"role": "user", "content": context})
    messages.append({"role": "user", "content": user})
    return messages
