from __future__ import annotations

from typing import Iterable, List

from translation_client import translate_texts as deepl_translate_texts
from translation_models import BatchTranslationResult, normalize_texts


def batch_translate(texts: Iterable[str], source_language: str, target_language: str) -> BatchTranslationResult:
    normalized = normalize_texts(texts)
    translated_texts = deepl_translate_texts(normalized, source_language, target_language)
    return BatchTranslationResult(
        translated_texts=translated_texts,
        source_language=source_language,
        target_language=target_language,
        provider="deepl",
        metadata={"model": "deepl-pro", "count": len(translated_texts)},
    )
