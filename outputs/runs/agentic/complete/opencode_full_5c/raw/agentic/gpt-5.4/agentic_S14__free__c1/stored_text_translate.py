from __future__ import annotations

from storage_client import get_translate_client
from storage_models import TranslationResult


def translate_extracted_text(
    text: str, target_language: str, source_language: str = "auto"
) -> TranslationResult:
    translate = get_translate_client()
    response = translate.translate_text(
        Text=text,
        SourceLanguageCode=source_language,
        TargetLanguageCode=target_language,
    )
    return TranslationResult(
        source_text=text,
        translated_text=response["TranslatedText"],
        source_language=response.get("SourceLanguageCode"),
        target_language=response["TargetLanguageCode"],
    )
