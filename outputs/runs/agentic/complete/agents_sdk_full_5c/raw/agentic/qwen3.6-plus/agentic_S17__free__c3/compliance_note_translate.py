"""
Translate encryption or compliance notes for reviewers using AWS Translate.

Uses the Amazon Translate API (translate.{region}.amazonaws.com) with the
boto3 SDK to translate cryptographic audit notes, compliance documentation,
and security findings into reviewer-specified languages.
"""

import os
import logging
from typing import Optional, Dict, Any, List

import boto3
from botocore.config import Config
from botocore.exceptions import ClientError

from security_models import (
    ComplianceTranslationRequest,
    ComplianceTranslationResponse,
)

logger = logging.getLogger(__name__)

TRANSLATE_ENDPOINT_TEMPLATE = "translate.{region}.amazonaws.com"
SUPPORTED_LANGUAGE_CODES = [
    "en", "es", "fr", "de", "ja", "ko", "pt", "zh", "ar", "hi",
    "it", "nl", "ru", "sv", "pl", "tr", "id", "ms", "th", "vi",
]


def get_translate_client(region: Optional[str] = None):
    """
    Initialize an Amazon Translate boto3 client.

    Provider: Amazon Translate (translate.{region}.amazonaws.com)
    """
    resolved_region = region or os.environ.get("AWS_DEFAULT_REGION", "us-east-1")
    credentials = {}
    access_key = os.environ.get("AWS_ACCESS_KEY_ID")
    secret_key = os.environ.get("AWS_SECRET_ACCESS_KEY")
    if access_key:
        credentials["aws_access_key_id"] = access_key
    if secret_key:
        credentials["aws_secret_access_key"] = secret_key

    config = Config(
        retries={"max_attempts": 3, "mode": "standard"},
        connect_timeout=5,
        read_timeout=30,
    )

    return boto3.client(
        "translate",
        region_name=resolved_region,
        config=config,
        **credentials,
    )


def translate_compliance_note(
    text: str,
    target_language: str,
    source_language: str = "en",
    client=None,
    region: Optional[str] = None,
) -> ComplianceTranslationResponse:
    """
    Translate an encryption or compliance note using Amazon Translate.

    Provider: Amazon Translate (translate.{region}.amazonaws.com)
    API: translate.translate_text

    Args:
        text: The compliance note or encryption documentation to translate.
        target_language: Target ISO 639-1 language code (e.g., 'es', 'fr').
        source_language: Source ISO 639-1 language code (default: 'en').
        client: Optional pre-initialized Translate client.
        region: Optional AWS region override.

    Returns:
        ComplianceTranslationResponse with translated text.

    Raises:
        ValueError: If text is empty or language codes invalid.
        ClientError: On Translate API failure.
    """
    if not text or len(text.strip()) == 0:
        raise ValueError("text cannot be empty")

    if target_language not in SUPPORTED_LANGUAGE_CODES:
        raise ValueError(
            f"Unsupported target language: {target_language}. "
            f"Must be one of: {SUPPORTED_LANGUAGE_CODES}"
        )

    if source_language not in SUPPORTED_LANGUAGE_CODES:
        source_language = "auto"

    resolved_region = region or os.environ.get("AWS_DEFAULT_REGION", "us-east-1")
    endpoint = TRANSLATE_ENDPOINT_TEMPLATE.format(region=resolved_region)

    if client is None:
        client = get_translate_client(resolved_region)

    logger.info(
        "Calling Amazon Translate (endpoint: %s, source: %s, target: %s)",
        endpoint,
        source_language,
        target_language,
    )

    translate_params = {
        "Text": text,
        "TargetLanguageCode": target_language,
    }

    if source_language != "auto":
        translate_params["SourceLanguageCode"] = source_language

    response = client.translate_text(**translate_params)

    translated_text = response.get("TranslatedText", "")
    detected_source = response.get("SourceLanguageCode", source_language)

    result = ComplianceTranslationResponse(
        translated_text=translated_text,
        target_language=target_language,
        source_language=detected_source,
        model="amazon_translate",
    )

    logger.info(
        "Translation completed via Amazon Translate: %s -> %s (%d chars)",
        detected_source,
        target_language,
        len(translated_text),
    )

    return result


def translate_from_request(
    request: ComplianceTranslationRequest, client=None
) -> ComplianceTranslationResponse:
    """
    Translate using a ComplianceTranslationRequest dataclass.

    Args:
        request: ComplianceTranslationRequest with text and language info.
        client: Optional pre-initialized Translate client.

    Returns:
        ComplianceTranslationResponse with translated text.
    """
    return translate_compliance_note(
        text=request.text,
        target_language=request.target_language,
        source_language=request.source_language,
        client=client,
    )


def batch_translate_notes(
    notes: List[str],
    target_language: str,
    source_language: str = "en",
    region: Optional[str] = None,
) -> List[ComplianceTranslationResponse]:
    """
    Translate multiple compliance notes using Amazon Translate.

    Provider: Amazon Translate (translate.{region}.amazonaws.com)

    Args:
        notes: List of note strings to translate.
        target_language: Target language code.
        source_language: Source language code (default: 'en').
        region: Optional AWS region override.

    Returns:
        List of ComplianceTranslationResponse objects.
    """
    client = get_translate_client(region)
    results = []

    for i, note in enumerate(notes):
        try:
            result = translate_compliance_note(
                text=note,
                target_language=target_language,
                source_language=source_language,
                client=client,
                region=region,
            )
            results.append(result)
        except ClientError as e:
            logger.warning("Failed to translate note %d: %s", i + 1, str(e))
            continue

    return results


def translate_compliance_document(
    document: str,
    target_language: str,
    source_language: str = "en",
    max_segment_length: int = 4500,
    region: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """
    Translate a large compliance document by segmenting it.

    Provider: Amazon Translate (translate.{region}.amazonaws.com)

    Splits a large document into segments under the Amazon Translate
    character limit (5000 characters per segment) and translates each.

    Args:
        document: The full compliance document text.
        target_language: Target language code.
        source_language: Source language code (default: 'en').
        max_segment_length: Maximum segment length (default: 4500).
        region: Optional AWS region override.

    Returns:
        List of dictionaries with segment, translation, and position info.
    """
    segments = []
    start = 0

    while start < len(document):
        end = start + max_segment_length
        # Try to break at sentence boundary
        if end < len(document):
            last_period = document.rfind(".", start + 100, end)
            if last_period > start:
                end = last_period + 1
            else:
                last_newline = document.rfind("\n", start, end)
                if last_newline > start:
                    end = last_newline + 1

        segment = document[start:end].strip()
        if segment:
            try:
                translation = translate_compliance_note(
                    text=segment,
                    target_language=target_language,
                    source_language=source_language,
                    region=region,
                )
                segments.append({
                    "position": {"start": start, "end": end},
                    "source": segment,
                    "translated": translation.translated_text,
                    "target_language": target_language,
                })
            except ClientError as e:
                logger.warning(
                    "Failed to translate segment at position %d: %s", start, str(e)
                )
                segments.append({
                    "position": {"start": start, "end": end},
                    "source": segment,
                    "translated": None,
                    "error": str(e),
                })

        start = end

    return segments


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    sample_note = os.environ.get(
        "COMPLIANCE_TRANSLATE_TEST_NOTE",
        "All encryption keys must be rotated every 90 days per SOC 2 Type II requirements."
    )
    target_lang = os.environ.get("TARGET_LANGUAGE", "es")
    if sample_note:
        result = translate_compliance_note(sample_note, target_language=target_lang)
        print(f"Source ({result.source_language}): {sample_note}")
        print(f"Target ({result.target_language}): {result.translated_text}")
    else:
        print("Set COMPLIANCE_TRANSLATE_TEST_NOTE environment variable to test.")
