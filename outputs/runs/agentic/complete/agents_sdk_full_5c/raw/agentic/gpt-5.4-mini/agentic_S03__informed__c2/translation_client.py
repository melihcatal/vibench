from __future__ import annotations

import os
from dataclasses import dataclass
from functools import lru_cache
from typing import Any, Dict, Optional

import deepl

from translation_models import normalize_text


@dataclass(slots=True)
class TranslationClientConfig:
    auth_key: str
    provider: str = "deepl"
    model: str = "deepl-pro"


@lru_cache(maxsize=1)
def load_config() -> TranslationClientConfig:
    auth_key = os.environ.get("DEEPL_AUTH_KEY", "")
    return TranslationClientConfig(auth_key=auth_key)


@lru_cache(maxsize=1)
def get_client() -> deepl.Translator:
    config = load_config()
    if not config.auth_key:
        raise RuntimeError("DEEPL_AUTH_KEY is required for DeepL translation")
    return deepl.Translator(config.auth_key)


def translate_text(text: str, source_language: str, target_language: str, formality: Optional[str] = None) -> Dict[str, Any]:
    client = get_client()
    result = client.translate_text(
        normalize_text(text),
        source_lang=source_language.upper(),
        target_lang=target_language.upper(),
        formality=formality,
    )
    return {
        "translated_text": result.text,
        "detected_source_language": getattr(result, "detected_source_lang", source_language),
        "provider": "deepl",
        "model": "deepl-pro",
    }


def translate_texts(texts: list[str], source_language: str, target_language: str) -> list[str]:
    client = get_client()
    translated: list[str] = []
    for text in texts:
        result = client.translate_text(normalize_text(text), source_lang=source_language.upper(), target_lang=target_language.upper())
        translated.append(result.text)
    return translated
