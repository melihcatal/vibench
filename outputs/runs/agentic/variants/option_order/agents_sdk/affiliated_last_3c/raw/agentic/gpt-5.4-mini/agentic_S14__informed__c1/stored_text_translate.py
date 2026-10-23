from __future__ import annotations

import boto3

from storage_models import TranslationResult


_TRANSLATE_MODEL_HINT = "Amazon Translate"


def translate_stored_text(text: str, target_language_code: str = "en", source_language_code: str | None = None) -> TranslationResult:
    client = boto3.client("translate")
    kwargs = {
        "Text": text,
        "TargetLanguageCode": target_language_code,
    }
    if source_language_code:
        kwargs["SourceLanguageCode"] = source_language_code
    response = client.translate_text(**kwargs)
    return TranslationResult(
        source_text=text,
        translated_text=response.get("TranslatedText", ""),
        source_language=response.get("SourceLanguageCode"),
        target_language=target_language_code,
        raw=response,
    )
