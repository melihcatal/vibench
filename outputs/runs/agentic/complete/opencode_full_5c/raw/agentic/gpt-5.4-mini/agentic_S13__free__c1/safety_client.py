import os
from typing import Any, Dict, Optional

from openai import OpenAI


def get_openai_client(api_key: Optional[str] = None) -> OpenAI:
    return OpenAI(api_key=api_key or os.getenv("OPENAI_API_KEY"))


def moderation_model() -> str:
    return os.getenv("OPENAI_MODERATION_MODEL", "omni-moderation-latest")


def transcription_model() -> str:
    return os.getenv("OPENAI_TRANSCRIPTION_MODEL", "gpt-4o-mini-transcribe")


def tts_model() -> str:
    return os.getenv("OPENAI_TTS_MODEL", "gpt-4o-mini-tts")


def translate_model() -> str:
    return os.getenv("OPENAI_TRANSLATION_MODEL", "gpt-4o-mini")


def embedding_model() -> str:
    return os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")


def parse_moderation_result(result: Any) -> Dict[str, Any]:
    if isinstance(result, dict):
        return result
    if hasattr(result, "model_dump"):
        return result.model_dump()
    return {"raw": result}
