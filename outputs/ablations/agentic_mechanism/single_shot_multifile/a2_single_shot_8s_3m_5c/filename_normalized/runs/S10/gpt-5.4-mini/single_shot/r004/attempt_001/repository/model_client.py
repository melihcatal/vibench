import os
from functools import lru_cache
from typing import Optional
from openai import OpenAI

DEFAULT_TEXT_MODEL = os.getenv("OPENAI_TEXT_MODEL", "gpt-4o-mini")
DEFAULT_SAFETY_MODEL = os.getenv("OPENAI_SAFETY_MODEL", "gpt-4o-mini")
DEFAULT_TRANSLATION_MODEL = os.getenv("OPENAI_TRANSLATION_MODEL", "gpt-4o-mini")
DEFAULT_EMBEDDING_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")
DEFAULT_TTS_MODEL = os.getenv("OPENAI_TTS_MODEL", "gpt-4o-mini-tts")


@lru_cache(maxsize=1)
def get_openai_client() -> OpenAI:
    return OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def select_text_model(model: Optional[str] = None, task: str = "text") -> str:
    if model:
        return model
    mapping = {
        "summarization": DEFAULT_TEXT_MODEL,
        "json_extraction": DEFAULT_TEXT_MODEL,
        "qa": DEFAULT_TEXT_MODEL,
        "streaming": DEFAULT_TEXT_MODEL,
        "safety": DEFAULT_SAFETY_MODEL,
        "translation": DEFAULT_TRANSLATION_MODEL,
        "embedding": DEFAULT_EMBEDDING_MODEL,
        "tts": DEFAULT_TTS_MODEL,
    }
    return mapping.get(task, DEFAULT_TEXT_MODEL)
