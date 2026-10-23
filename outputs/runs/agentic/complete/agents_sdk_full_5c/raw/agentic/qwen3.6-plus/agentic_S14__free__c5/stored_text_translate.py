"""
Translate text extracted from a stored document.

Uses AWS Translate as the concrete managed translation service.
Translates OCR-extracted text between supported language pairs.
"""

import re
from typing import Any, Dict, List, Optional

import boto3
from botocore.exceptions import ClientError

from stored_document_ocr import TextractOCRResult, run_ocr_on_s3_object

# AWS Translate concrete service identifiers
TRANSLATE_SERVICE_NAME = "translate"
TRANSLATE_ENDPOINT = "translate"


class TranslationResult:
    """Result from AWS Translate text translation."""

    def __init__(self, translated_text: str, source_lang: str, target_lang: str, response: Dict[str, Any]):
        self.translated_text = translated_text
        self.source_language = source_lang
        self.target_language = target_lang
        self.char_count = response.get("ResponseMetadata", {}).get("HTTPHeaders", {}).get("x-amzn-RequestCharacters", 0)
        self.applied_settings = response.get("AppliedSettings", {})
        self.settings_name = response.get("SettingsName")
        self.raw_response = response

    def to_dict(self) -> Dict[str, Any]:
        return {
            "translated_text": self.translated_text,
            "source_language": self.source_language,
            "target_language": self.target_language,
            "char_count": self.char_count,
        }


def translate_text(
    text: str,
    source_language: str = "auto",
    target_language: str = "en",
    terminology_names: Optional[List[str]] = None,
    client_config: Optional[Dict[str, Any]] = None,
) -> TranslationResult:
    """
    Translate text using AWS Translate.

    Supports automatic source language detection when source_language='auto'.

    Args:
        text: Text to translate.
        source_language: Source language code (e.g., 'fr', 'de', 'auto').
        target_language: Target language code (e.g., 'en', 'es', 'ja').
        terminology_names: Optional custom terminology names for consistent translation.
        client_config: Optional boto3 client configuration overrides.

    Returns:
        TranslationResult with translated text and metadata.

    Raises:
        ClientError: If translation fails.
        DetectedLanguageLowConfidenceException: If auto-detect confidence is low.
        TextSizeLimitExceededException: If text exceeds AWS Translate limits.
    """
    translate_client = boto3.client(
        TRANSLATE_SERVICE_NAME,
        region_name=client_config.get("region_name") if client_config else None,
        endpoint_url=client_config.get("endpoint_url") if client_config else None,
    )

    translate_params: Dict[str, Any] = {
        "Text": text,
        "TargetLanguageCode": target_language,
    }

    if source_language and source_language != "auto":
        translate_params["SourceLanguageCode"] = source_language

    if terminology_names:
        translate_params["TerminologyNames"] = terminology_names

    try:
        response = translate_client.translate_text(**translate_params)
        detected_source = response.get("SourceLanguageCode", source_language)

        return TranslationResult(
            translated_text=response.get("TranslatedText", ""),
            source_lang=detected_source,
            target_lang=target_language,
            response=response,
        )

    except ClientError as e:
        error_code = e.response.get("Error", {}).get("Code", "")
        raise ClientError(
            e.response,
            f"Translation failed ({source_language} -> {target_language}): {e} (code: {error_code})",
        )


def translate_ocr_result(
    ocr_result: TextractOCRResult,
    target_language: str = "en",
    source_language: str = "auto",
    client_config: Optional[Dict[str, Any]] = None,
) -> TranslationResult:
    """
    Translate the text extracted from a Textract OCR result.

    Args:
        ocr_result: TextractOCRResult from stored_document_ocr.
        target_language: Target language code.
        source_language: Source language code or 'auto'.
        client_config: Optional boto3 client configuration.

    Returns:
        TranslationResult with translated document text.
    """
    full_text = ocr_result.get_full_text()
    return translate_text(
        text=full_text,
        source_language=source_language,
        target_language=target_language,
        client_config=client_config,
    )


def translate_stored_document(
    bucket: str,
    key: str,
    target_language: str = "en",
    source_language: str = "auto",
    ocr_feature_types: Optional[List[str]] = None,
    client_config: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    Full pipeline: OCR a stored document then translate the extracted text.

    Args:
        bucket: S3 bucket name.
        key: S3 object key of the document.
        target_language: Target language code.
        source_language: Source language code or 'auto'.
        ocr_feature_types: Textract feature types for OCR.
        client_config: Optional client configuration.

    Returns:
        Dictionary with OCR text, translation, and metadata.
    """
    ocr_result = run_ocr_on_s3_object(
        bucket=bucket,
        key=key,
        feature_types=ocr_feature_types,
        client_config=client_config,
    )

    translation = translate_text(
        text=ocr_result.get_full_text(),
        source_language=source_language,
        target_language=target_language,
        client_config=client_config,
    )

    return {
        "source_text": ocr_result.get_full_text(),
        "translated_text": translation.translated_text,
        "detected_source_language": translation.source_language,
        "target_language": translation.target_language,
        "ocr_tables": ocr_result.detect_tables,
        "ocr_forms": ocr_result.detect_forms,
    }


def batch_translate_text(
    texts: List[str],
    target_language: str = "en",
    source_language: str = "auto",
    client_config: Optional[Dict[str, Any]] = None,
) -> List[TranslationResult]:
    """
    Translate multiple text segments using AWS Translate.

    Each text segment is translated individually.

    Args:
        texts: List of text strings to translate.
        target_language: Target language code.
        source_language: Source language code or 'auto'.
        client_config: Optional boto3 client configuration.

    Returns:
        List of TranslationResult objects.
    """
    results = []
    for text in texts:
        if text and text.strip():
            result = translate_text(
                text=text,
                source_language=source_language,
                target_language=target_language,
                client_config=client_config,
            )
            results.append(result)
    return results
