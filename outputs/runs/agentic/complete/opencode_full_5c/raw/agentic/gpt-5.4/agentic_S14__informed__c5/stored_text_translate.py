from __future__ import annotations

from storage_client import get_translate_client
from storage_models import TranslationResult


def translate_stored_text(
    text: str, target_language: str, source_language: str | None = None
) -> TranslationResult:
    translate = get_translate_client()
    params = {
        "Text": text,
        "TargetLanguageCode": target_language,
    }
    if source_language:
        params["SourceLanguageCode"] = source_language
    response = translate.translate_text(**params)
    return TranslationResult(
        source_language=response.get("SourceLanguageCode"),
        target_language=response["TargetLanguageCode"],
        translated_text=response["TranslatedText"],
        provider="amazon-translate",
    )
