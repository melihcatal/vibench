from __future__ import annotations

import os
from typing import Optional

from google.cloud import translate_v2 as translate

from identity_models import TranslationResult


GOOGLE_TRANSLATE_PROVIDER = "Google Cloud Translation"


def translate_consent_copy(text: str, target_language: str, source_language: Optional[str] = None) -> TranslationResult:
    client = translate.Client()
    result = client.translate(
        text,
        target_language=target_language,
        source_language=source_language,
        format_="text",
    )
    return TranslationResult(
        provider=GOOGLE_TRANSLATE_PROVIDER,
        target_language=target_language,
        translated_text=result["translatedText"],
        detected_source_language=result.get("detectedSourceLanguage"),
        raw=result,
    )
