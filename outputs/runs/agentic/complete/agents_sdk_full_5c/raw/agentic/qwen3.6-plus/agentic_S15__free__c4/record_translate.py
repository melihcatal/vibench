"""
Translate user-facing document fields using AWS Translate.
Uses the boto3 AWS SDK for Amazon Translate managed translation service.
"""

from __future__ import annotations

import os
from typing import Any, Optional

import boto3
from botocore.exceptions import ClientError

AWS_REGION_ENV = "AWS_DEFAULT_REGION"
AWS_TRANSLATE_TARGET_LANGUAGE_CODE = "es"  # Spanish as default target language
AWS_TRANSLATE_SOURCE_LANGUAGE_CODE = "en"  # English as default source language


def _get_translate_client() -> boto3.client:
    """Create and return a boto3 client for Amazon Translate."""
    region = os.environ.get(AWS_REGION_ENV, "us-east-1")
    return boto3.client("translate", region_name=region)


def translate_text(
    text: str,
    target_language_code: str = AWS_TRANSLATE_TARGET_LANGUAGE_CODE,
    source_language_code: str = AWS_TRANSLATE_SOURCE_LANGUAGE_CODE,
    client: Optional[Any] = None,
) -> dict[str, Any]:
    """
    Translate a single text string using Amazon Translate.
    
    Args:
        text: The source text to translate.
        target_language_code: The target language code (e.g., 'es', 'fr', 'de').
        source_language_code: The source language code (default: 'en').
        client: Optional pre-configured boto3 Translate client.
    
    Returns:
        A dict with the translated text, detected language, and original text.
    """
    if client is None:
        client = _get_translate_client()

    try:
        response = client.translate_text(
            Text=text,
            SourceLanguageCode=source_language_code,
            TargetLanguageCode=target_language_code,
        )
        return {
            "original_text": text,
            "translated_text": response["TranslatedText"],
            "source_language": source_language_code,
            "target_language": target_language_code,
        }
    except ClientError as e:
        raise RuntimeError(f"Amazon Translate API error: {e}")


def translate_document_fields(
    document: dict[str, Any],
    fields_to_translate: list[str],
    target_language_code: str = AWS_TRANSLATE_TARGET_LANGUAGE_CODE,
    source_language_code: str = AWS_TRANSLATE_SOURCE_LANGUAGE_CODE,
    client: Optional[Any] = None,
) -> dict[str, Any]:
    """
    Translate specified user-facing fields within a document record using Amazon Translate.
    
    Args:
        document: A document record dict with a 'content' sub-dict.
        fields_to_translate: List of field names within 'content' to translate.
        target_language_code: The target language code.
        source_language_code: The source language code.
        client: Optional pre-configured boto3 Translate client.
    
    Returns:
        A dict with the document ID, translated fields, and a new document content dict.
    """
    if client is None:
        client = _get_translate_client()

    content = document.get("content", {})
    translated_content = dict(content)
    translations: dict[str, dict[str, Any]] = {}

    for field_name in fields_to_translate:
        value = content.get(field_name)
        if isinstance(value, str) and value.strip():
            result = translate_text(
                text=value,
                target_language_code=target_language_code,
                source_language_code=source_language_code,
                client=client,
            )
            translated_content[field_name] = result["translated_text"]
            translations[field_name] = result

    return {
        "doc_id": document.get("doc_id"),
        "translated_content": translated_content,
        "translations": translations,
        "target_language": target_language_code,
        "source_language": source_language_code,
    }


def batch_translate_texts(
    texts: list[str],
    target_language_code: str = AWS_TRANSLATE_TARGET_LANGUAGE_CODE,
    source_language_code: str = AWS_TRANSLATE_SOURCE_LANGUAGE_CODE,
    client: Optional[Any] = None,
) -> list[dict[str, Any]]:
    """
    Translate a batch of text strings using Amazon Translate.
    
    Args:
        texts: A list of source text strings to translate.
        target_language_code: The target language code.
        source_language_code: The source language code.
        client: Optional pre-configured boto3 Translate client.
    
    Returns:
        A list of translation result dicts, one per input text.
    """
    if client is None:
        client = _get_translate_client()

    results = []
    for text in texts:
        if isinstance(text, str) and text.strip():
            result = translate_text(
                text=text,
                target_language_code=target_language_code,
                source_language_code=source_language_code,
                client=client,
            )
            results.append(result)
        else:
            results.append({
                "original_text": text,
                "translated_text": text,
                "source_language": source_language_code,
                "target_language": target_language_code,
            })

    return results


def detect_source_language(
    text: str,
    client: Optional[Any] = None,
) -> dict[str, Any]:
    """
    Detect the source language of a text string using Amazon Translate's auto-detection.
    
    Args:
        text: The text to analyze for language detection.
        client: Optional pre-configured boto3 Translate client.
    
    Returns:
        A dict with the detected language code and original text.
    """
    if client is None:
        client = _get_translate_client()

    try:
        response = client.translate_text(
            Text=text,
            SourceLanguageCode="auto",
            TargetLanguageCode=AWS_TRANSLATE_TARGET_LANGUAGE_CODE,
        )
        return {
            "original_text": text,
            "detected_source_language": response["SourceLanguageCode"],
        }
    except ClientError as e:
        raise RuntimeError(f"Amazon Translate auto-detection error: {e}")


if __name__ == "__main__":
    sample_doc = {
        "doc_id": "doc-to-translate-001",
        "content": {
            "title": "Welcome to Our Service",
            "description": "This is a user-facing description of the product.",
        },
    }
    result = translate_document_fields(
        document=sample_doc,
        fields_to_translate=["title", "description"],
        target_language_code="fr",
    )
    print(result)
