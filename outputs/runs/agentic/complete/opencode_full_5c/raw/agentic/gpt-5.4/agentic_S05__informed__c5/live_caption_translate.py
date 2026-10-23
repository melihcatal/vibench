from __future__ import annotations

import os
from typing import Iterable, List

import deepl


def create_translator(auth_key: str | None = None) -> deepl.Translator:
    key = auth_key or os.getenv("DEEPL_AUTH_KEY")
    if not key:
        raise ValueError("DEEPL_AUTH_KEY is required")
    return deepl.Translator(key)


def translate_live_captions(captions: Iterable[str], target_language: str) -> List[str]:
    translator = create_translator()
    results = translator.translate_text(list(captions), target_lang=target_language)
    if isinstance(results, list):
        return [item.text for item in results]
    return [results.text]
