from __future__ import annotations

import boto3

from security_models import TranslationRequest


AWS_TRANSLATE_PROVIDER = "boto3:translate"


def compliance_note_translate(request: TranslationRequest, region: str = "us-east-1") -> str:
    client = boto3.client("translate", region_name=region)
    response = client.translate_text(
        Text=request.text,
        SourceLanguageCode=request.source_language,
        TargetLanguageCode=request.target_language,
    )
    return response.get("TranslatedText", "") + f" | provider={AWS_TRANSLATE_PROVIDER}"
