from __future__ import annotations

from typing import Any

import boto3

from storage_models import TranslationRequest, TranslationResult, coerce_text


def translate_stored_text(request: TranslationRequest) -> TranslationResult:
    # Amazon Translate
    translate = boto3.client("translate")
    kwargs: dict[str, Any] = {"Text": request.text, "TargetLanguageCode": request.target_language}
    if request.source_language:
        kwargs["SourceLanguageCode"] = request.source_language
    response = translate.translate_text(**kwargs)
    return TranslationResult(translated_text=coerce_text(response.get("TranslatedText")), raw=response)
