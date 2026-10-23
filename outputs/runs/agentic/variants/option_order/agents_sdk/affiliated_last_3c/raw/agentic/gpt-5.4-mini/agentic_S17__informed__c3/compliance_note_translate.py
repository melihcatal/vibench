from __future__ import annotations

import os

import boto3

from security_models import TranslationResult, normalize_text

PROVIDER = "amazon-translate"


def translate_compliance_note(note: str, source_language: str | None = None, target_language: str | None = None) -> TranslationResult:
    client = boto3.client("translate", region_name=os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION"))
    src = source_language or os.getenv("TRANSLATION_SOURCE_LANG", "en")
    tgt = target_language or os.getenv("TRANSLATION_TARGET_LANG", "es")
    response = client.translate_text(Text=normalize_text(note), SourceLanguageCode=src, TargetLanguageCode=tgt)
    return TranslationResult(provider=PROVIDER, source_language=src, target_language=tgt, translated_text=response.get("TranslatedText", ""), metadata=response)
