from __future__ import annotations

from typing import Any, Dict, Iterable, List

import deepl


def translate_transcript_segments(
    segments: Iterable[Dict[str, Any]],
    target_language: str,
    source_language: str | None = None,
) -> Dict[str, Any]:
    translator = deepl.Translator(
        auth_key=__import__("os").getenv("DEEPL_AUTH_KEY", "")
    )
    texts = [segment.get("text", "") for segment in segments]
    if not translator.auth_key:
        raise RuntimeError("DEEPL_AUTH_KEY is required")
    results = translator.translate_text(
        texts,
        target_lang=target_language,
        source_lang=source_language,
        model_type="prefer_quality_optimized",
    )
    if not isinstance(results, list):
        results = [results]
    translated_segments: List[Dict[str, Any]] = []
    for segment, result in zip(segments, results):
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
