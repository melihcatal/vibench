from __future__ import annotations

from typing import Iterable, List, Sequence

import deepl


def translate_transcript(segments: Sequence[str] | Iterable[str], target_lang: str, source_lang: str | None = None) -> dict:
    auth_key = __import__("os").getenv("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY is required")
    translator = deepl.Translator(auth_key)
    texts: List[str] = [segment for segment in segments]
    result = translator.translate_text(texts, target_lang=target_lang, source_lang=source_lang)
    results = result if isinstance(result, list) else [result]
    return {
        "provider": "DeepL",
        "target_lang": target_lang,
        "translations": [item.text for item in results],
        "detected_source_langs": [getattr(item, "detected_source_lang", None) for item in results],
    }
