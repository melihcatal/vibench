from __future__ import annotations

import os
from typing import Dict, Iterable, List

import deepl


DEEPL_AUTH_KEY = os.getenv("DEEPL_AUTH_KEY")


def translate_transcript(segments: Iterable[Dict[str, object]], target_language: str, source_language: str | None = None) -> Dict[str, object]:
    if not DEEPL_AUTH_KEY:
        raise ValueError("DEEPL_AUTH_KEY is required")
    translator = deepl.Translator(DEEPL_AUTH_KEY)
    segment_list: List[Dict[str, object]] = list(segments)
    texts = [str(segment.get("text", "")) for segment in segment_list]
    results = translator.translate_text(texts, target_lang=target_language, source_lang=source_language)
    translated_segments = []
    for segment, result in zip(segment_list, results):
        translated_segments.append(
            {
                **segment,
                "translated_text": result.text,
                "detected_source_language": result.detected_source_lang,
            }
        )
    return {
        "provider": "DeepL API",
        "target_language": target_language,
        "segments": translated_segments,
    }
