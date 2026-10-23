"""
Translate user-facing document fields using Amazon Translate.
Connects to the Amazon Translate hosted service for machine translation
of document content into target languages.
"""

import os
from typing import Any, Dict, List, Optional

import boto3
from botocore.exceptions import ClientError


AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID", "")
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY", "")
AWS_REGION = os.environ.get("AWS_REGION", "us-east-1")

DEFAULT_SOURCE_LANGUAGE = "en"
DEFAULT_TARGET_LANGUAGE = "es"


def _get_translate_client():
    """Create and return a boto3 translate client for Amazon Translate."""
    return boto3.client(
        "translate",
        region_name=AWS_REGION,
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    )


def translate_text(
    text: str,
    target_language_code: str = DEFAULT_TARGET_LANGUAGE,
    source_language_code: str = DEFAULT_SOURCE_LANGUAGE,
) -> str:
    """
    Translate a single text string using Amazon Translate.

    Args:
        text: The text to translate.
        target_language_code: ISO 639-1 language code for the target language.
        source_language_code: ISO 639-1 language code for the source language.

    Returns:
        The translated text string.
    """
    if not text or not text.strip():
        return text

    client = _get_translate_client()

    try:
        response = client.translate_text(
            Text=text,
            SourceLanguageCode=source_language_code,
            TargetLanguageCode=target_language_code,
        )
        return response.get("TranslatedText", text)
    except ClientError:
        return text


def translate_document_fields(
    document: Dict[str, Any],
    fields: List[str],
    target_language_code: str = DEFAULT_TARGET_LANGUAGE,
    source_language_code: str = DEFAULT_SOURCE_LANGUAGE,
) -> Dict[str, Any]:
    """
    Translate specified fields of a document record using Amazon Translate.

    Args:
        document: The document dict containing text fields to translate.
        fields: List of field names whose values should be translated.
        target_language_code: Target ISO 639-1 language code.
        source_language_code: Source ISO 639-1 language code.

    Returns:
        A new document dict with translated field values under keys
        like '<field>_<target_language_code>'.
    """
    translated = dict(document)

    for field_name in fields:
        if field_name not in document:
            continue

        original_value = document[field_name]
        if not isinstance(original_value, str) or not original_value.strip():
            translated[field_name] = original_value
            continue

        translated_text = translate_text(
            original_value,
            target_language_code=target_language_code,
            source_language_code=source_language_code,
        )
        translated_key = f"{field_name}_{target_language_code}"
        translated[translated_key] = translated_text

    return translated


def translate_documents_batch(
    documents: List[Dict[str, Any]],
    fields: List[str],
    target_language_code: str = DEFAULT_TARGET_LANGUAGE,
    source_language_code: str = DEFAULT_SOURCE_LANGUAGE,
) -> List[Dict[str, Any]]:
    """
    Translate specified fields across a list of documents using Amazon Translate.

    Args:
        documents: List of document dicts.
        fields: Field names to translate in each document.
        target_language_code: Target language code.
        source_language_code: Source language code.

    Returns:
        List of document dicts with translated fields added.
    """
    results = []
    for doc in documents:
        translated = translate_document_fields(
            doc,
            fields=fields,
            target_language_code=target_language_code,
            source_language_code=source_language_code,
        )
        results.append(translated)
    return results
