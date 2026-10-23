from __future__ import annotations

import os

import boto3

from storage_models import TranslationResult


def translate_extracted_text(
    text: str, target_language: str, source_language: str = "auto"
) -> TranslationResult:
    region_name = (
        os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION") or "us-east-1"
    )
    translate = boto3.client("translate", region_name=region_name)
    response = translate.translate_text(
        Text=text,
        SourceLanguageCode=source_language,
        TargetLanguageCode=target_language,
    )
    return TranslationResult(
        source_text=text,
        translated_text=response["TranslatedText"],
        target_language=target_language,
        provider="amazon_translate",
    )
