from __future__ import annotations

import os
from typing import Iterable, List

import deepl

from speech_models import normalize_transcript_text


def translate_live_captions(
    captions: Iterable[str],
    *,
    target_language: str,
    source_language: str | None = None,
    model_type: str = "prefer_quality_optimized",
) -> List[str]:
    auth_key = os.getenv("DEEPL_AUTH_KEY")
    if not auth_key:
        raise RuntimeError("DEEPL_AUTH_KEY is required")
    translator = deepl.Translator(auth_key)
    translated: list[str] = []
    for caption in captions:
        text = normalize_transcript_text(caption)
        if not text:
            continue
        result = translator.translate_text(
            text,
            source_lang=source_language,
            target_lang=target_language,
            model_type=model_type,
        )
        translated.append(result.text)
    return translated
