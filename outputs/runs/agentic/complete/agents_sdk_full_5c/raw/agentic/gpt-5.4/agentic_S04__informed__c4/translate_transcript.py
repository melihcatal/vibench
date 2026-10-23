from __future__ import annotations

from typing import Iterable, List

import deepl

from speech_models import TranslationSegment


DEEPL_MODEL_TYPE = "quality_optimized"


def translate_transcript(segments: Iterable[str], target_language: str) -> List[TranslationSegment]:
    auth_key = __import__("os").getenv("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY is required")
    translator = deepl.Translator(auth_key)
    texts = list(segments)
    results = translator.translate_text(texts, target_lang=target_language, model_type=DEEPL_MODEL_TYPE)
    if not isinstance(results, list):
        results = [results]
    return [
        TranslationSegment(text=source, translated_text=result.text, target_language=target_language)
        for source, result in zip(texts, results)
    ]
