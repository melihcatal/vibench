"""
Translate text extracted from a stored document using AWS Translate.

Uses the Amazon Translate service (boto3 translate client) to translate
text content between supported language pairs.
"""

import os
from typing import Optional, List, Dict, Any

import boto3
from botocore.exceptions import ClientError

from stored_document_ocr import OcrResult, run_ocr_on_stored_document

AWS_TRANSLATE_REGION = os.environ.get("AWS_TRANSLATE_REGION", os.environ.get("AWS_DEFAULT_REGION", "us-east-1"))
AWS_TRANSLATE_TERMINOLOGY_NAME = os.environ.get("AWS_TRANSLATE_TERMINOLOGY_NAME", None)


class TranslationResult:
    """Result of a text translation operation."""

    def __init__(
        self,
        translated_text: str,
        source_language: str,
        target_language: str,
        confidence: Optional[float] = None,
        source_bucket: Optional[str] = None,
        source_key: Optional[str] = None,
    ):
        self.translated_text = translated_text
        self.source_language = source_language
        self.target_language = target_language
        self.confidence = confidence
        self.source_bucket = source_bucket
        self.source_key = source_key

    def to_dict(self) -> Dict[str, Any]:
        return {
            "translated_text": self.translated_text,
            "source_language": self.source_language,
            "target_language": self.target_language,
            "confidence": self.confidence,
            "source_bucket": self.source_bucket,
            "source_key": self.source_key,
        }


class DocumentTranslationResult:
    """Complete translation result for a document."""

    def __init__(
        self,
        results: List[TranslationResult],
        combined_text: str,
        block_translations: Optional[List[Dict[str, Any]]] = None,
        source_bucket: Optional[str] = None,
        source_key: Optional[str] = None,
    ):
        self.results = results
        self.combined_text = combined_text
        self.block_translations = block_translations or []
        self.source_bucket = source_bucket
        self.source_key = source_key

    def to_dict(self) -> Dict[str, Any]:
        return {
            "combined_text": self.combined_text,
            "translation_count": len(self.results),
            "results": [r.to_dict() for r in self.results],
            "block_translations": self.block_translations,
            "source_bucket": self.source_bucket,
            "source_key": self.source_key,
        }


def _get_translate_client() -> boto3.client:
    """Create and return an AWS Translate client."""
    # Provider signal: boto3 translate client (Amazon Translate)
    session = boto3.Session(region_name=AWS_TRANSLATE_REGION)
    return session.client("translate")


def translate_text(
    text: str,
    source_language_code: str = "auto",
    target_language_code: str = "en",
    terminology_name: Optional[str] = None,
    translate_client=None,
) -> TranslationResult:
    """
    Translate text using Amazon Translate.

    Args:
        text: Text to translate
        source_language_code: Source language code or "auto" for auto-detection
        target_language_code: Target language code (e.g., "en", "es", "fr")
        terminology_name: Optional custom terminology name
        translate_client: Pre-configured boto3 translate client

    Returns:
        TranslationResult with translated text and metadata
    """
    client = translate_client or _get_translate_client()

    params: Dict[str, Any] = {
        "Text": text,
        "TargetLanguageCode": target_language_code,
    }

    if source_language_code and source_language_code != "auto":
        params["SourceLanguageCode"] = source_language_code

    if terminology_name or AWS_TRANSLATE_TERMINOLOGY_NAME:
        params["TerminologyNames"] = [terminology_name or AWS_TRANSLATE_TERMINOLOGY_NAME]

    try:
        response = client.translate_text(**params)

        return TranslationResult(
            translated_text=response.get("TranslatedText", ""),
            source_language=response.get("SourceLanguageCode", source_language_code),
            target_language=response.get("TargetLanguageCode", target_language_code),
            confidence=None,  # Amazon Translate does not return confidence scores
        )

    except ClientError as e:
        raise RuntimeError(f"Amazon Translate error: {e}") from e


def translate_stored_document(
    key: str,
    target_language_code: str = "en",
    source_language_code: str = "auto",
    bucket: Optional[str] = None,
    translate_blocks: bool = False,
    s3_client=None,
    translate_client=None,
) -> DocumentTranslationResult:
    """
    OCR a stored document and translate the extracted text.

    Args:
        key: S3 object key of the document
        target_language_code: Target language for translation
        source_language_code: Source language or "auto"
        bucket: S3 bucket name
        translate_blocks: Whether to translate individual OCR blocks
        s3_client: Pre-configured boto3 S3 client
        translate_client: Pre-configured boto3 translate client

    Returns:
        DocumentTranslationResult with translated content
    """
    # Step 1: Run OCR on the stored document using Google Cloud Vision
    ocr_result = run_ocr_on_stored_document(key, bucket=bucket, s3_client=s3_client)

    results = []
    block_translations = []

    if translate_blocks and ocr_result.blocks:
        # Translate each OCR block individually
        for block in ocr_result.blocks:
            if block.text.strip():
                translation = translate_text(
                    text=block.text,
                    source_language_code=source_language_code,
                    target_language_code=target_language_code,
                    translate_client=translate_client,
                )
                translation.source_bucket = ocr_result.source_bucket
                translation.source_key = ocr_result.source_key
                results.append(translation)
                block_translations.append({
                    "original": block.text,
                    "translated": translation.translated_text,
                    "source_language": translation.source_language,
                    "block_type": block.block_type,
                })
        combined_text = " ".join([r.translated_text for r in results])
    else:
        # Translate the full document text
        if ocr_result.full_text.strip():
            translation = translate_text(
                text=ocr_result.full_text,
                source_language_code=source_language_code,
                target_language_code=target_language_code,
                translate_client=translate_client,
            )
            translation.source_bucket = ocr_result.source_bucket
            translation.source_key = ocr_result.source_key
            results.append(translation)
            combined_text = translation.translated_text
        else:
            combined_text = ""

    return DocumentTranslationResult(
        results=results,
        combined_text=combined_text,
        block_translations=block_translations,
        source_bucket=ocr_result.source_bucket,
        source_key=ocr_result.source_key,
    )
