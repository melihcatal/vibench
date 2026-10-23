import os
from typing import Dict, List, Optional

import boto3
from botocore.exceptions import BotoCoreError, ClientError


def translate_text(
    text: str,
    source_lang: str,
    target_lang: str,
    region: Optional[str] = None,
    settings: Optional[Dict] = None,
) -> str:
    """
    Translates a single text string using Amazon Translate.

    Args:
        text: The text to translate.
        source_lang: The source language code (e.g., 'en').
        target_lang: The target language code (e.g., 'es').
        region: AWS region (e.g., 'us-east-1').
        settings: Optional settings for translation (e.g., formality, profanity handling).

    Returns:
        The translated text.

    Raises:
        ValueError: If translation fails due to invalid input or AWS service error.
    """
    if not text.strip():
        return text

    region = region or os.getenv("AWS_REGION", "us-east-1")
    client = boto3.client("translate", region_name=region)

    try:
        response = client.translate_text(
            Text=text,
            SourceLanguageCode=source_lang,
            TargetLanguageCode=target_lang,
            Settings=settings or {},
        )
        return response["TranslatedText"]
    except (BotoCoreError, ClientError, KeyError) as e:
        raise ValueError(f"Failed to translate text: {e}")
