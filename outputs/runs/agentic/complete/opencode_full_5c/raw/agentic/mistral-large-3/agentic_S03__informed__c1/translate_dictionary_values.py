import os
from typing import Dict, List, Optional

import boto3
from botocore.exceptions import BotoCoreError, ClientError


def translate_dictionary_values(
    dictionary: Dict[str, str],
    source_lang: str,
    target_lang: str,
    region: Optional[str] = None,
    settings: Optional[dict] = None,
) -> Dict[str, str]:
    """
    Translates dictionary values while preserving keys using Amazon Translate.

    Args:
        dictionary: Dictionary with keys to preserve and values to translate.
        source_lang: The source language code (e.g., 'en').
        target_lang: The target language code (e.g., 'es').
        region: AWS region (e.g., 'us-east-1').
        settings: Optional settings for translation (e.g., formality, profanity handling).

    Returns:
        Dictionary with translated values and original keys.

    Raises:
        ValueError: If translation fails due to invalid input or AWS service error.
    """
    if not dictionary:
        return {}

    region = region or os.getenv("AWS_REGION", "us-east-1")
    client = boto3.client("translate", region_name=region)

    try:
        translated_dict = {}
        for key, value in dictionary.items():
            if not value.strip():
                translated_dict[key] = value
                continue
            response = client.translate_text(
                Text=value,
                SourceLanguageCode=source_lang,
                TargetLanguageCode=target_lang,
                Settings=settings or {},
            )
            translated_dict[key] = response["TranslatedText"]
        return translated_dict
    except (BotoCoreError, ClientError, KeyError) as e:
        raise ValueError(f"Failed to translate dictionary values: {e}")
