from __future__ import annotations

import boto3

from storage_models import TranslationRequest, TranslationResult


def stored_text_translate(request: TranslationRequest, region_name: str | None = None) -> TranslationResult:
    client = boto3.client("translate", region_name=region_name)
    kwargs = {"Text": request.text, "SourceLanguageCode": request.source_language or "auto", "TargetLanguageCode": request.target_language}
    response = client.translate_text(**kwargs)
    return TranslationResult(
        source_text=request.text,
        translated_text=response["TranslatedText"],
        source_language=response.get("SourceLanguageCode", request.source_language),
        target_language=response.get("TargetLanguageCode", request.target_language),
    )
