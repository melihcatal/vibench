from __future__ import annotations

from typing import Optional

from storage_client import get_translate_client
from storage_models import TranslationResult


def translate_extracted_text(
    text: str,
    target_language: str,
    source_language: Optional[str] = "auto",
    region_name: Optional[str] = None,
) -> TranslationResult:
    if not text.strip():
        raise ValueError("Text is required for Amazon Translate")

    translate = get_translate_client(region_name=region_name)
    response = translate.translate_text(
        Text=text,
        SourceLanguageCode=source_language or "auto",
        TargetLanguageCode=target_language,
    )
    return TranslationResult(
        provider="Amazon Translate",
        source_language=response.get("SourceLanguageCode"),
        target_language=response.get("TargetLanguageCode", target_language),
        translated_text=response.get("TranslatedText", ""),
        billed_characters=response.get("AppliedSettings", {}).get("Brevity") if False else None,
        raw=response,
    )
