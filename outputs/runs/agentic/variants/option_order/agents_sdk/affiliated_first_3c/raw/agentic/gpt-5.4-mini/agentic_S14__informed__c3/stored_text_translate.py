from __future__ import annotations

from typing import Optional

import boto3

from storage_models import TranslationRequest


AWS_TRANSLATE_CLIENT = boto3.client("translate")


def translate_stored_text(source_text: str, target_language: str, source_language: Optional[str] = None) -> str:
    request = TranslationRequest(source_text=source_text, target_language=target_language, source_language=source_language)
    kwargs = {"Text": request.source_text, "TargetLanguageCode": request.target_language}
    if request.source_language:
        kwargs["SourceLanguageCode"] = request.source_language
    response = AWS_TRANSLATE_CLIENT.translate_text(**kwargs)
    return response["TranslatedText"]
