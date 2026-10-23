from __future__ import annotations

import os

import boto3

from observability_models import TranslationResponse


def dashboard_note_translate(source_text: str, target_locale: str = "es") -> TranslationResponse:
    region = os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION") or "us-east-1"
    client = boto3.client("translate", region_name=region)
    translated = client.translate_text(Text=source_text, SourceLanguageCode="auto", TargetLanguageCode=target_locale)
    return TranslationResponse(source_text=source_text, target_locale=target_locale, translated_text=translated.get("TranslatedText", ""))
