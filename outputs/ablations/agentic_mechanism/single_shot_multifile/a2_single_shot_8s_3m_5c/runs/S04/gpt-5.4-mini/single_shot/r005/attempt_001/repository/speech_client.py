import os
from dataclasses import dataclass
from functools import lru_cache
from typing import Optional

from openai import OpenAI


@dataclass(frozen=True)
class SpeechSettings:
    openai_api_key: str
    transcription_model: str
    translation_model: str
    moderation_model: str
    embedding_model: str


@lru_cache(maxsize=1)
def load_speech_settings() -> SpeechSettings:
    return SpeechSettings(
        openai_api_key=os.environ.get("OPENAI_API_KEY", ""),
        transcription_model=os.environ.get("OPENAI_TRANSCRIPTION_MODEL", "gpt-4o-transcribe"),
        translation_model=os.environ.get("OPENAI_TRANSLATION_MODEL", "gpt-4.1-mini"),
        moderation_model=os.environ.get("OPENAI_MODERATION_MODEL", "omni-moderation-latest"),
        embedding_model=os.environ.get("OPENAI_EMBEDDING_MODEL", "text-embedding-3-large"),
    )


def get_openai_client(settings: Optional[SpeechSettings] = None) -> OpenAI:
    resolved = settings or load_speech_settings()
    return OpenAI(api_key=resolved.openai_api_key)
