import boto3
from security_models import TranslationRequest, TranslationResponse
from typing import Optional


def translate_compliance_note(request: TranslationRequest, region_name: str) -> TranslationResponse:
    client = boto3.client("translate", region_name=region_name)

    response = client.translate_text(
        Text=request.text,
        SourceLanguageCode=request.source_language or "auto",  # "auto" for automatic source language detection
        TargetLanguageCode=request.target_language
    )

    return TranslationResponse(
        translated_text=response["TranslatedText"],
        source_language=response["SourceLanguageCode"],
        target_language=response["TargetLanguageCode"]
    )
