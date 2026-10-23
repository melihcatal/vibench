from __future__ import annotations

from typing import Optional

from storage_client import get_translate_client
from storage_models import TranslationResult


def translate_extracted_text(text: str, target_language: str, source_language: str = "auto", region: Optional[str] = None) -> TranslationResult:
    if not text.strip():
        raise ValueError("text must not be empty")

    translate = get_translate_client(region=region)
    response = translate.translate_text(
        Text=text,
        SourceLanguageCode=source_language,
        TargetLanguageCode=target_language,
    )
    return TranslationResult(
        provider="aws_translate",
        source_language=response.get("SourceLanguageCode"),
        target_language=response["TargetLanguageCode"],
        translated_text=response["TranslatedText"],
    )
