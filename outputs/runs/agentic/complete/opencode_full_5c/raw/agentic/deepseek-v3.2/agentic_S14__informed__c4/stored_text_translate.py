import boto3
import os
from typing import Optional
from botocore.exceptions import ClientError
from storage_client import get_translate_client
from storage_models import TranslationResult


def translate_text(
    text: str, target_language_code: str, source_language_code: Optional[str] = None
) -> TranslationResult:
    """
    Translate text using Amazon Translate.

    Args:
        text: Text to translate
        target_language_code: Target language code (e.g., 'es', 'fr', 'de')
        source_language_code: Source language code (optional, auto-detected if not provided)

    Returns:
        TranslationResult with translated text and metadata
    """
    translate_client = get_translate_client()

    try:
        translate_kwargs = {"Text": text, "TargetLanguageCode": target_language_code}

        if source_language_code:
            translate_kwargs["SourceLanguageCode"] = source_language_code

        response = translate_client.translate_text(**translate_kwargs)

        return TranslationResult(
            success=True,
            translated_text=response["TranslatedText"],
            source_language=response.get("SourceLanguageCode"),
            target_language=response["TargetLanguageCode"],
        )

    except ClientError as e:
        error_code = e.response["Error"]["Code"]
        error_msg = e.response["Error"]["Message"]
        return TranslationResult(
            success=False, error=f"Translate error ({error_code}): {error_msg}"
        )
    except Exception as e:
        return TranslationResult(success=False, error=f"Unexpected error: {str(e)}")


def translate_document_text(
    bucket_name: str,
    object_key: str,
    target_language_code: str,
    source_language_code: Optional[str] = None,
) -> TranslationResult:
    """
    Translate text extracted from a document stored in S3.

    Args:
        bucket_name: S3 bucket name containing the document
        object_key: S3 object key of the document
        target_language_code: Target language code (e.g., 'es', 'fr', 'de')
        source_language_code: Source language code (optional, auto-detected if not provided)

    Returns:
        TranslationResult with translated text and metadata
    """
    # First extract text using OCR
    from stored_document_ocr import extract_text_from_s3_document

    ocr_result = extract_text_from_s3_document(bucket_name, object_key)

    if not ocr_result.success:
        return TranslationResult(success=False, error=f"OCR failed: {ocr_result.error}")

    if not ocr_result.text:
        return TranslationResult(success=False, error="No text extracted from document")

    # Translate the extracted text
    return translate_text(ocr_result.text, target_language_code, source_language_code)


def detect_language(text: str) -> dict:
    """
    Detect the language of text using Amazon Translate.

    Args:
        text: Text to analyze

    Returns:
        Dictionary with language detection results
    """
    translate_client = get_translate_client()

    try:
        response = translate_client.detect_dominant_language(Text=text)

        languages = response.get("Languages", [])
        if languages:
            primary_language = max(languages, key=lambda x: x["Score"])
            return {
                "success": True,
                "language_code": primary_language["LanguageCode"],
                "confidence": primary_language["Score"],
                "all_languages": languages,
            }
        else:
            return {"success": False, "error": "No language detected"}

    except ClientError as e:
        error_code = e.response["Error"]["Code"]
        error_msg = e.response["Error"]["Message"]
        return {
            "success": False,
            "error": f"Translate error ({error_code}): {error_msg}",
        }
    except Exception as e:
        return {"success": False, "error": f"Unexpected error: {str(e)}"}


def batch_translate_texts(
    texts: list, target_language_code: str, source_language_code: Optional[str] = None
) -> list:
    """
    Translate multiple texts in batch.

    Args:
        texts: List of texts to translate
        target_language_code: Target language code
        source_language_code: Source language code (optional)

    Returns:
        List of TranslationResult objects
    """
    results = []
    for text in texts:
        result = translate_text(text, target_language_code, source_language_code)
        results.append(result)
    return results
