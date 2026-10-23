from __future__ import annotations

import os
from typing import Dict, List

import deepl

from speech_models import TranscriptResult


def translate_transcript(
    result: TranscriptResult, target_language: str
) -> List[Dict[str, str]]:
    auth_key = os.getenv("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY is required")
    translator = deepl.Translator(auth_key)
    translated: List[Dict[str, str]] = []
    source_segments = result.utterances or result.segments
    for segment in source_segments:
        response = translator.translate_text(
            segment.text,
            target_lang=target_language,
            model_type="quality_optimized",
        )
        translated.append(
            {
                "text": segment.text,
                "translated_text": response.text,
                "target_language": target_language,
            }
        )
    return translated
