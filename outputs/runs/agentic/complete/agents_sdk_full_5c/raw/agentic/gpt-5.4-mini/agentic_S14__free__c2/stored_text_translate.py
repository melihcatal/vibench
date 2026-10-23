from __future__ import annotations

from typing import Optional

from storage_client import get_translate_client
from storage_models import TranslationResult


def stored_text_translate(text: str, target_language: str, source_language: Optional[str] = None) -> TranslationResult:
    client = get_translate_client()
    params = {"Text": text, "TargetLanguageCode": target_language}
    if source_language:
        params["SourceLanguageCode"] = source_language
    response = client.translate_text(**params)
    return TranslationResult(
        source_language=response.get("SourceLanguageCode", source_language),
        target_language=response.get("TargetLanguageCode", target_language),
        translated_text=response.get("TranslatedText", ""),
    )
