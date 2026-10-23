import os
from dataclasses import dataclass
from typing import Optional

from openai import OpenAI


@dataclass(frozen=True)
class TranslationClientConfig:
    model: str = os.getenv("OPENAI_TRANSLATION_MODEL", "gpt-4.1-mini")


def get_openai_client() -> OpenAI:
    return OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def get_translation_model() -> str:
    return TranslationClientConfig().model


def normalize_language(language: Optional[str]) -> str:
    return (language or "").strip()
