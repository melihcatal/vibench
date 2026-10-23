import os
from typing import Dict, Optional
from translation_client import TranslationClient


def translate_dictionary_values(
    dictionary: Dict[str, str],
    target_language: str,
    source_language: Optional[str] = None,
) -> Dict[str, str]:
    """
    Translate dictionary values while preserving keys.

    Args:
        dictionary: Dictionary with string values to translate
        target_language: Target language code (e.g., 'es', 'fr', 'de')
        source_language: Optional source language code (e.g., 'en')

    Returns:
        Dictionary with same keys and translated values
    """
    client = TranslationClient()

    # Use Amazon Translate for batch translation of dictionary values
    import boto3

    # Initialize Amazon Translate client
    translate_client = boto3.client(
        "translate",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        region_name=os.getenv("AWS_REGION", "us-east-1"),
    )

    # Extract values and translate them
    keys = list(dictionary.keys())
    values = list(dictionary.values())

    translated_dict = {}

    # Process values in batches (Amazon Translate supports up to 100 items per batch)
    batch_size = 100
    for i in range(0, len(values), batch_size):
        batch_values = values[i : i + batch_size]

        # Translate batch
        if source_language:
            response = translate_client.translate_text(
                TextList=batch_values,
                SourceLanguageCode=source_language,
                TargetLanguageCode=target_language,
            )
        else:
            # Auto-detect source language
            response = translate_client.translate_text(
                TextList=batch_values, TargetLanguageCode=target_language
            )

        # Map translated values back to keys
        translated_batch = response["TranslatedTextList"]
        for j, key in enumerate(keys[i : i + batch_size]):
            translated_dict[key] = translated_batch[j]

    return translated_dict
