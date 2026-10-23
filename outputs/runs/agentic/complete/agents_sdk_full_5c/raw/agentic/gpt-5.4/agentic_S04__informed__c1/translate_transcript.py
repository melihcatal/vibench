from __future__ import annotations

import os
from typing import Dict, List, Sequence

import deepl


def translate_transcript(
    segments: Sequence[str],
    target_lang: str,
    source_lang: str | None = None,
) -> Dict[str, List[Dict[str, str]]]:
    auth_key = os.environ.get("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY is required")
    client = deepl.Translator(auth_key)
    result: List[Dict[str, str]] = []
    for text in segments:
        translated = client.translate_text(text, target_lang=target_lang, source_lang=source_lang)
        result.append(
            {
                "source_text": text,
                "translated_text": translated.text,
                "detected_source_lang": getattr(translated, "detected_source_lang", source_lang or ""),
            }
        )
    return {
        "provider": "DeepL",
        "target_lang": target_lang,
        "translations": result,
    }
