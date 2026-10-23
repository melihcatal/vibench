"""
alt_text_translate.py - Translate generated image descriptions
using AWS Translate service.

Provider: AWS Translate (boto3 SDK)
API hostname: https://translate.{region}.amazonaws.com
"""

import os
from typing import List, Dict, Optional

import boto3
from botocore.config import Config

from describe_image import describe_image, describe_image_from_bytes

AWS_TRANSLATE_REGION = os.environ.get("AWS_REGION", "us-east-1")
AWS_TRANSLATE_MODEL_FAMILY = "nmt"  # Neural Machine Translation via AWS Translate


def get_translate_client() -> boto3.client:
    """Create and return a configured AWS Translate client."""
    session = boto3.Session(
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
        region_name=AWS_TRANSLATE_REGION,
    )
    config = Config(
        retries={"max_attempts": 3, "mode": "adaptive"},
        connect_timeout=10,
        read_timeout=30,
    )
    return session.client("translate", config=config)


def translate_alt_text(
    description: str,
    source_language: str = "en",
    target_language: str = "es",
) -> str:
    """
    Translate an image description (alt text) using AWS Translate.

    Args:
        description: The image description to translate.
        source_language: Source language code (e.g., 'en' for English).
        target_language: Target language code (e.g., 'es' for Spanish).

    Returns:
        Translated description string.
    """
    client = get_translate_client()

    response = client.translate_text(
        Text=description,
        SourceLanguageCode=source_language,
        TargetLanguageCode=target_language,
    )

    return response.get("TranslatedText", description)


def generate_and_translate_alt_text(
    image_path: str,
    target_languages: Optional[List[str]] = None,
    source_language: str = "en",
    min_confidence: float = 50.0,
) -> Dict[str, str]:
    """
    Generate an image description and translate it into multiple languages.

    Uses AWS Rekognition to describe the image, then AWS Translate to produce
    translations in the specified target languages.

    Args:
        image_path: Path to the local image file.
        target_languages: List of target language codes. Defaults to ['es', 'fr', 'de', 'ja'].
        source_language: Source language code.
        min_confidence: Confidence threshold for Rekognition.

    Returns:
        Dictionary mapping language codes to translated descriptions.
    """
    if target_languages is None:
        target_languages = ["es", "fr", "de", "ja"]

    description_response = describe_image(
        image_path, min_confidence=min_confidence
    )
    original_description = description_response.description

    translations: Dict[str, str] = {
        source_language: original_description,
    }

    for target_lang in target_languages:
        translated = translate_alt_text(
            original_description,
            source_language=source_language,
            target_language=target_lang,
        )
        translations[target_lang] = translated

    return translations


def batch_translate_alt_texts(
    descriptions: List[str],
    target_language: str = "es",
    source_language: str = "en",
) -> List[str]:
    """
    Translate multiple image descriptions using AWS Translate batch processing.

    Uses Amazon Translate to translate a list of descriptions in a single call.

    Args:
        descriptions: List of image descriptions to translate.
        target_language: Target language code.
        source_language: Source language code.

    Returns:
        List of translated descriptions.
    """
    client = get_translate_client()

    translated_texts = []
    for desc in descriptions:
        response = client.translate_text(
            Text=desc,
            SourceLanguageCode=source_language,
            TargetLanguageCode=target_language,
        )
        translated_texts.append(response.get("TranslatedText", desc))

    return translated_texts
