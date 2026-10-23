import os
from typing import List, Optional

import boto3
from botocore.exceptions import BotoCoreError, ClientError


def batch_translate(
    texts: List[str],
    source_lang: str,
    target_lang: str,
    region: Optional[str] = None,
    settings: Optional[dict] = None,
) -> List[str]:
    """
    Translates a list of text strings using Amazon Translate while preserving order.

    Args:
        texts: List of texts to translate.
        source_lang: The source language code (e.g., 'en').
        target_lang: The target language code (e.g., 'es').
        region: AWS region (e.g., 'us-east-1').
        settings: Optional settings for translation (e.g., formality, profanity handling).

    Returns:
        List of translated texts in the same order as input.

    Raises:
        ValueError: If translation fails due to invalid input or AWS service error.
    """
    if not texts:
        return []

    region = region or os.getenv("AWS_REGION", "us-east-1")
    client = boto3.client("translate", region_name=region)

    try:
        results = []
        for text in texts:
            if not text.strip():
                results.append(text)
                continue
            response = client.translate_text(
                Text=text,
                SourceLanguageCode=source_lang,
                TargetLanguageCode=target_lang,
                Settings=settings or {},
            )
            results.append(response["TranslatedText"])
        return results
    except (BotoCoreError, ClientError, KeyError) as e:
        raise ValueError(f"Failed to batch translate texts: {e}")
