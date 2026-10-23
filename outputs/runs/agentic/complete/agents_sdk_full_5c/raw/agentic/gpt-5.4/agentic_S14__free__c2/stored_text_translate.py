from __future__ import annotations

from typing import Optional

from storage_client import get_translate_client
from storage_models import TranslationResult


def translate_extracted_text(
    text: str,
    target_language_code: str,
    source_language_code: Optional[str] = "auto",
) -> TranslationResult:
    translate = get_translate_client()
    response = translate.translate_text(
        Text=text,
        SourceLanguageCode=source_language_code or "auto",
        TargetLanguageCode=target_language_code,
    )
    return TranslationResult(
        translated_text=response["TranslatedText"],
        source_language_code=response.get("SourceLanguageCode"),
        target_language_code=response.get("TargetLanguageCode", target_language_code),
    )
