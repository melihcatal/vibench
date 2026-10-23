"""
stored_text_translate.py - Translate text extracted from a stored document
using Amazon Translate.

Uses the boto3 SDK (Amazon Translate).
Auth env vars: AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY
"""
from __future__ import annotations

import os
from typing import Optional

import boto3
from botocore.exceptions import ClientError

from storage_models import TranslateRequest, TranslateResponse


def stored_text_translate(
    text: str,
    target_language: str = "en",
    source_language: str = "auto",
    terminology_name: Optional[str] = None,
    aws_access_key_id: Optional[str] = None,
    aws_secret_access_key: Optional[str] = None,
    region: Optional[str] = None,
) -> TranslateResponse:
    """
    Translate text extracted from a stored document using Amazon Translate.

    Amazon Translate is a neural machine translation service that delivers
    fast, high-quality, and affordable language translation.

    Args:
        text: The source text to translate.
        target_language: Target language code (e.g., "en", "es", "fr", "de", "ja").
        source_language: Source language code, or "auto" for automatic detection.
        terminology_name: Optional custom terminology name for domain-specific translations.
        aws_access_key_id: Optional AWS access key ID override.
        aws_secret_access_key: Optional AWS secret access key override.
        region: Optional AWS region override.

    Returns:
        TranslateResponse with translated text and detected source language.
    """
    request = TranslateRequest(
        text=text,
        source_language=source_language,
        target_language=target_language,
        terminology_name=terminology_name,
    )

    translate_region = region or os.environ.get("AWS_DEFAULT_REGION", "us-east-1")
    translate_client = boto3.client(
        "translate",
        region_name=translate_region,
        aws_access_key_id=aws_access_key_id or os.environ.get("AWS_ACCESS_KEY_ID", ""),
        aws_secret_access_key=aws_secret_access_key or os.environ.get("AWS_SECRET_ACCESS_KEY", ""),
    )

    translate_kwargs = {
        "Text": request.text,
        "SourceLanguageCode": request.source_language,
        "TargetLanguageCode": request.target_language,
    }

    # Add custom terminology if specified
    if request.terminology_name:
        translate_kwargs["TerminologyNames"] = [request.terminology_name]

    try:
        response = translate_client.translate_text(**translate_kwargs)

        # Amazon Translate returns the detected source language when "auto" is used
        detected_source = response.get("SourceLanguageCode", request.source_language)

        return TranslateResponse(
            translated_text=response["TranslatedText"],
            source_language=detected_source,
            target_language=request.target_language,
        )

    except ClientError as e:
        error_code = e.response.get("Error", {}).get("Code", "Unknown")
        error_message = e.response.get("Error", {}).get("Message", str(e))
        raise RuntimeError(
            f"Amazon Translate error [{error_code}]: {error_message}"
        )


def batch_translate_texts(
    texts: list[str],
    target_language: str = "en",
    source_language: str = "auto",
    aws_access_key_id: Optional[str] = None,
    aws_secret_access_key: Optional[str] = None,
    region: Optional[str] = None,
) -> list[TranslateResponse]:
    """
    Translate a batch of texts using Amazon Translate.

    Args:
        texts: List of source texts to translate.
        target_language: Target language code.
        source_language: Source language code or "auto".
        aws_access_key_id: Optional AWS access key ID override.
        aws_secret_access_key: Optional AWS secret access key override.
        region: Optional AWS region override.

    Returns:
        List of TranslateResponse objects, one per input text.
    """
    results = []
    for text in texts:
        result = stored_text_translate(
            text=text,
            target_language=target_language,
            source_language=source_language,
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            region=region,
        )
        results.append(result)
    return results
