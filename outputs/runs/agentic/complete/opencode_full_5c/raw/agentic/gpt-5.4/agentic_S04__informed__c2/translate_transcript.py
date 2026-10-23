from __future__ import annotations

from typing import Iterable, List

import deepl


def translate_transcript(
    segments: Iterable[str], target_language: str, source_language: str | None = None
) -> List[str]:
    translator = deepl.Translator(__import__("os").environ["DEEPL_AUTH_KEY"])
    results = translator.translate_text(
        list(segments), target_lang=target_language, source_lang=source_language
    )
    if isinstance(results, list):
        return [item.text for item in results]
    return [results.text]
