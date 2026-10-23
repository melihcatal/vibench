import os
from typing import List
import boto3
from aws_encryption_sdk import KMSMasterKeyProvider

# LATER-STEP: ocr_translate.py

# Provider: Amazon Translate
# Credentials should be set via AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY


def translate_text(source_text: str, target_language: str = "es") -> str:
    """Translate extracted OCR text using Amazon Translate.

    Args:
        source_text (str): Text to translate.
        target_language (str): Target language code (e.g., 'es' for Spanish).

    Returns:
        str: Translated text.
    """
    translate = boto3.client("translate")
    response = translate.translate_text(
        Text=source_text, SourceLanguageCode="en", TargetLanguageCode=target_language
    )
    return response.get("TranslatedText", "")


# Example batch translation (optional)
def translate_batch(texts: List[str], target_language: str = "es") -> List[str]:
    translate = boto3.client("translate")
    results = []
    for txt in texts:
        res = translate.translate_text(
            Text=txt, SourceLanguageCode="en", TargetLanguageCode=target_language
        )
        results.append(res.get("TranslatedText", ""))
    return results
