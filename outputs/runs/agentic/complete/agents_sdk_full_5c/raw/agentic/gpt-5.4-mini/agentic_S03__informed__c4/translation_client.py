from __future__ import annotations

import os
from functools import lru_cache
from typing import Any

from deepl import Translator

from translation_models import normalize_text

DEEPL_MODEL = "deepl-api"


@lru_cache(maxsize=1)
def get_deepl_translator() -> Translator:
    auth_key = os.environ.get("DEEPL_AUTH_KEY")
    if not auth_key:
        raise RuntimeError("DEEPL_AUTH_KEY is required for DeepL translation")
    return Translator(auth_key)


def translate_text(text: str, source_language: str, target_language: str, glossary: dict[str, str] | None = None, formality: str | None = None) -> str:
    client = get_deepl_translator()
    kwargs: dict[str, Any] = {"source_lang": source_language.upper(), "target_lang": target_language.upper()}
    if formality:
        kwargs["formality"] = formality
    if glossary:
        kwargs["glossary"] = glossary
    result = client.translate_text(normalize_text(text), **kwargs)
    return str(result)


def translate_texts(texts: list[str], source_language: str, target_language: str) -> list[str]:
    client = get_deepl_translator()
    results = client.translate_text(
        [normalize_text(text) for text in texts],
        source_lang=source_language.upper(),
        target_lang=target_language.upper(),
    )
    return [str(item) for item in results]
