from __future__ import annotations

import os
from typing import Iterable, List

import deepl



def translate_user_fields(texts: Iterable[str], target_language: str, source_language: str | None = None) -> List[str]:
    auth_key = os.getenv("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY is required")
    translator = deepl.Translator(auth_key)
    results = translator.translate_text(list(texts), target_lang=target_language, source_lang=source_language)
    if not isinstance(results, list):
        results = [results]
    return [result.text for result in results]
