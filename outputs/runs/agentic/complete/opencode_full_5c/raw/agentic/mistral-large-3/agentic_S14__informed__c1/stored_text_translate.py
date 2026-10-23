import os
from typing import Optional

import boto3
from botocore.exceptions import ClientError


def translate_text_from_stored_document(
    text: str,
    source_language: str = "auto",
    target_language: str = "en",
) -> dict:
    """
    Translates text extracted from a stored document using Amazon Translate.

    Args:
        text: Text to translate.
        source_language: Source language code. Defaults to auto-detect.
        target_language: Target language code. Defaults to English.

    Returns:
        Dictionary containing translated text and metadata.
    """
    translate_client = boto3.client("translate")

    try:
        response = translate_client.translate_text(
            Text=text,
            SourceLanguageCode=source_language,
            TargetLanguageCode=target_language,
        )

        return {
            "translated_text": response["TranslatedText"],
            "source_language": response["SourceLanguageCode"],
            "target_language": response["TargetLanguageCode"],
            "provider": "aws_translate",
        }
    except ClientError as e:
        raise Exception(f"Failed to translate text: {e}")
