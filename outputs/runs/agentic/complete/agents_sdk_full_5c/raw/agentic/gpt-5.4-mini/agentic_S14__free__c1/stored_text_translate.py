from __future__ import annotations

import os

import boto3

from storage_client import normalize_boto_error
from storage_models import TranslationResult


translate = boto3.client("translate", region_name=os.environ.get("AWS_REGION", "us-east-1"))


def stored_text_translate(source_text: str, target_language: str = "en", source_language: str = "auto") -> dict:
    try:
        kwargs = {"Text": source_text, "TargetLanguageCode": target_language}
        if source_language != "auto":
            kwargs["SourceLanguageCode"] = source_language
        response = translate.translate_text(**kwargs)
        result = TranslationResult(
            source_text=source_text,
            translated_text=response.get("TranslatedText", ""),
            source_language=response.get("SourceLanguageCode"),
            target_language=response.get("TargetLanguageCode"),
        )
        return result.to_dict()
    except Exception as exc:
        return {"error": normalize_boto_error(exc)}
