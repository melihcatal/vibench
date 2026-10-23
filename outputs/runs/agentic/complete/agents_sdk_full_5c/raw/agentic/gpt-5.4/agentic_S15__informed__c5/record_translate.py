from __future__ import annotations

from typing import Iterable, List

import deepl
import os



def translate_texts(texts: Iterable[str], target_language: str, source_language: str | None = None) -> List[str]:
    translator = deepl.Translator(os.getenv("DEEPL_AUTH_KEY"))
    results = translator.translate_text(
        list(texts),
        target_lang=target_language,
        source_lang=source_language,
    )
    if isinstance(results, list):
        return [item.text for item in results]
    return [results.text]
