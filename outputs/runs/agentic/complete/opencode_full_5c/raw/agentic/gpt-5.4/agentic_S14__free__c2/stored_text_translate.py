from __future__ import annotations

from typing import Optional

from storage_client import get_translate_client
from storage_models import TranslationResult


def translate_stored_text(
    text: str, target_language: str, source_language: Optional[str] = "auto"
) -> TranslationResult:
    translate = get_translate_client()
    response = translate.translate_text(
        Text=text,
        SourceLanguageCode=source_language or "auto",
        TargetLanguageCode=target_language,
    )
    return TranslationResult(
        source_language=response.get("SourceLanguageCode"),
        target_language=response["TargetLanguageCode"],
        translated_text=response["TranslatedText"],
        provider="aws-translate",
    )
