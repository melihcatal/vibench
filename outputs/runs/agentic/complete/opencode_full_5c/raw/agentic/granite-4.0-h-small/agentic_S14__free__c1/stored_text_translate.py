# stored_text_translate.py
# [LATER-STEP] Translate text extracted from a stored document
# Using AWS Translate as the concrete translation provider
import boto3
from storage_models import DownloadResponse
from typing import Optional, Any


def translate_text(source_language: str, target_language: str, text: str) -> dict:
    """Translate text using AWS Translate.

    Args:
        source_language: ISO-639-1 code of source language (e.g., 'en').
        target_language: ISO-639-1 code of target language (e.g., 'es').
        text: Source text to translate.

    Returns:
        Parsed JSON response from AWS Translate.
    """
    translate = boto3.client("translate")
    response = translate.translate_text(
        SourceLanguageCode=source_language,
        TargetLanguageCode=target_language,
        Text=text,
    )
    return response
