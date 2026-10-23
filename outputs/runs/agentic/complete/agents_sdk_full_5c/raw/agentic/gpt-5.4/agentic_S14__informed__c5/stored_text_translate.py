from __future__ import annotations

import boto3
from typing import Optional

from storage_models import TranslationResult


def translate_extracted_text(
    text: str,
    target_language: str,
    source_language: Optional[str] = "auto",
    region_name: Optional[str] = None,
) -> TranslationResult:
    region = region_name or "us-east-1"
    client = boto3.session.Session(region_name=region).client("translate")
    response = client.translate_text(
        Text=text,
        SourceLanguageCode=source_language or "auto",
        TargetLanguageCode=target_language,
    )
    return TranslationResult(
        provider="amazon-translate",
        source_language=response.get("SourceLanguageCode"),
        target_language=response["TargetLanguageCode"],
        translated_text=response["TranslatedText"],
    )
