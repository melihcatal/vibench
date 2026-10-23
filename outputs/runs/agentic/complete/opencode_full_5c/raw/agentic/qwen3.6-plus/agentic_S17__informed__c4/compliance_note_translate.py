import os
import boto3
from botocore.exceptions import ClientError
from security_models import ComplianceTranslationRequest, ComplianceTranslationResponse
from security_client import get_translate_client


def translate_compliance_note(text, source_language="en", target_language="es"):
    request = ComplianceTranslationRequest(
        text=text,
        source_language=source_language,
        target_language=target_language,
    )
    client = get_translate_client()
    try:
        response = client.translate_text(
            Text=request.text,
            SourceLanguageCode=request.source_language,
            TargetLanguageCode=request.target_language,
        )
        return ComplianceTranslationResponse(
            translated_text=response.get("TranslatedText", ""),
            source_language=response.get("SourceLanguageCode", request.source_language),
            target_language=response.get("TargetLanguageCode", request.target_language),
            service="Amazon Translate",
        )
    except ClientError as e:
        raise RuntimeError(
            f"Compliance note translation failed: {e.response['Error']['Message']}"
        ) from e
