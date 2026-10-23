from __future__ import annotations

from typing import Iterable, List

from translation_client import translate_texts_with_deepl


def batch_translate(
    texts: Iterable[str],
    target_language: str,
    source_language: str | None = None,
    formality: str | None = None,
) -> List[str]:
    results = translate_texts_with_deepl(
        list(texts),
        source_language=source_language,
        target_language=target_language,
        formality=formality,
    )
    return [result.text for result in results]
