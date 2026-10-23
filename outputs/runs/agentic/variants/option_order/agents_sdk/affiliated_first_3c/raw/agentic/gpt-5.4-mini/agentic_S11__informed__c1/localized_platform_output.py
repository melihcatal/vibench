from __future__ import annotations

import os
from typing import Optional

from google.cloud import translate_v2 as translate

from model_models import TranslationResult


def translate_output(text: str, target_language: str = "es", source_language: Optional[str] = None) -> TranslationResult:
    client = translate.Client()
    result = client.translate(text, target_language=target_language, source_language=source_language)
    return TranslationResult(
        text=result["translatedText"],
        source_language=result.get("detectedSourceLanguage") or source_language,
        target_language=target_language,
        raw=result,
    )
