from __future__ import annotations

from typing import Dict, List, Optional

import deepl


def translate_transcript(
    segments: List[Dict[str, str]],
    target_language: str,
    source_language: Optional[str] = None,
) -> Dict[str, object]:
    auth_key = __import__("os").getenv("DEEPL_AUTH_KEY")
    if not auth_key:
        raise RuntimeError("DEEPL_AUTH_KEY is required")
    translator = deepl.Translator(auth_key)
    texts = [segment.get("text", "") for segment in segments]
    result = translator.translate_text(
        texts, target_lang=target_language, source_lang=source_language
    )
    translated_items = result if isinstance(result, list) else [result]
    translated_segments = []
    for segment, item in zip(segments, translated_items):
        updated = dict(segment)
        updated["translated_text"] = item.text
        updated["detected_source_language"] = getattr(
            item, "detected_source_lang", source_language
        )
        translated_segments.append(updated)
    return {
        "provider": "DeepL",
        "target_language": target_language,
        "segments": translated_segments,
    }
