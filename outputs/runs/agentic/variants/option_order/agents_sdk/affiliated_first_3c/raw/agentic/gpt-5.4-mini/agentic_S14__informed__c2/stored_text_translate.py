from __future__ import annotations

from typing import Optional

import boto3

from storage_models import TranslationRequest


translate = boto3.client("translate")


def stored_text_translate(source_text: str, target_language: str, source_language: Optional[str] = None) -> dict:
    request = TranslationRequest(source_text=source_text, target_language=target_language, source_language=source_language)
    kwargs = {"Text": request.source_text, "TargetLanguageCode": request.target_language}
    if request.source_language:
        kwargs["SourceLanguageCode"] = request.source_language
    response = translate.translate_text(**kwargs)
    return {"source_text": request.source_text, "translated_text": response.get("TranslatedText", ""), "target_language": request.target_language}
