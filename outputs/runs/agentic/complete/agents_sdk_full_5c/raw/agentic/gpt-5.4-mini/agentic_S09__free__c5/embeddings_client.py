import os
from dataclasses import dataclass
from functools import lru_cache
from typing import Optional

from openai import OpenAI

OPENAI_EMBEDDING_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")
OPENAI_CHAT_MODEL = os.getenv("OPENAI_CHAT_MODEL", "gpt-4o-mini")
OPENAI_TTS_MODEL = os.getenv("OPENAI_TTS_MODEL", "gpt-4o-mini-tts")
OPENAI_TRANSCRIPTION_MODEL = os.getenv("OPENAI_TRANSCRIPTION_MODEL", "whisper-1")


@dataclass(frozen=True)
class EmbeddingsConfig:
    api_key: Optional[str] = None
    organization: Optional[str] = None
    base_url: Optional[str] = None


@lru_cache(maxsize=1)
def get_client() -> OpenAI:
    kwargs = {}
    if os.getenv("OPENAI_API_KEY"):
        kwargs["api_key"] = os.getenv("OPENAI_API_KEY")
    if os.getenv("OPENAI_ORG_ID"):
        kwargs["organization"] = os.getenv("OPENAI_ORG_ID")
    if os.getenv("OPENAI_BASE_URL"):
        kwargs["base_url"] = os.getenv("OPENAI_BASE_URL")
    return OpenAI(**kwargs)
