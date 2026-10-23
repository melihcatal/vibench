"""
[LATER-STEP] Translate platform model output for another locale using
Amazon Translate.

Provider: Amazon Translate
SDK: boto3
Auth: AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY
"""

from __future__ import annotations

import os
from typing import Optional

import boto3
from botocore.config import Config


# Provider-specific configuration
TRANSLATE_REGION = os.environ.get("AWS_DEFAULT_REGION", "us-east-1")
AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID", "")
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY", "")

TRANSLATE_CONFIG = Config(
    retries={"max_attempts": 3, "mode": "adaptive"},
    read_timeout=60,
)

# Amazon Translate language codes (ISO 639-1)
SUPPORTED_LANGUAGES = {
    "en": "English",
    "es": "Spanish",
    "fr": "French",
    "de": "German",
    "ja": "Japanese",
    "zh": "Chinese (Simplified)",
    "ar": "Arabic",
    "pt": "Portuguese",
    "hi": "Hindi",
    "ko": "Korean",
    "ru": "Russian",
    "it": "Italian",
}


def get_translate_client(
    region_name: Optional[str] = None,
) -> boto3.client:
    """Create an Amazon Translate client.

    Provider signals: boto3 translate service, AWS credentials.
    """
    region = region_name or TRANSLATE_REGION
    if AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY:
        session = boto3.Session(
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
            region_name=region,
        )
    else:
        session = boto3.Session(region_name=region)
    return session.client("translate", config=TRANSLATE_CONFIG)


def translate_text(
    text: str,
    source_language: str = "auto",
    target_language: str = "es",
    region: Optional[str] = None,
) -> dict:
    """Translate text using Amazon Translate API.

    Provider signals: boto3 translate.translate_text, Amazon-specific
    parameters including TerminologyNames and Profanity settings.

    Amazon Translate auto-detects source language when source_language="auto".
    """
    client = get_translate_client(region_name=region)

    params = {
        "Text": text,
        "TargetLanguageCode": target_language,
    }

    if source_language and source_language != "auto":
        params["SourceLanguageCode"] = source_language
    else:
        # Amazon Translate supports auto-detection
        params["SourceLanguageCode"] = "auto"

    response = client.translate_text(**params)

    return {
        "translated_text": response.get("TranslatedText", ""),
        "source_language": response.get("SourceLanguageCode", source_language),
        "target_language": target_language,
        "provider": "amazon-translate",
    }


def translate_platform_output(
    model_output: str,
    target_locale: str = "es",
    source_locale: str = "auto",
    region: Optional[str] = None,
) -> dict:
    """Translate a managed model platform output to another locale.

    Provider: Amazon Translate.
    Returns the translated text along with locale metadata.
    """
    result = translate_text(
        text=model_output,
        source_language=source_locale,
        target_language=target_locale,
        region=region,
    )

    return {
        "original_text": model_output,
        "translated_text": result["translated_text"],
        "source_locale": result["source_language"],
        "target_locale": target_locale,
        "provider": "amazon-translate",
        "target_language_name": SUPPORTED_LANGUAGES.get(target_locale, target_locale),
    }


def translate_batch(
    texts: list[str],
    target_language: str = "es",
    source_language: str = "auto",
    region: Optional[str] = None,
) -> list[dict]:
    """Batch translate multiple texts using Amazon Translate.

    Provider signals: boto3 translate, Amazon Translate API.
    """
    results = []
    for text in texts:
        result = translate_text(
            text=text,
            source_language=source_language,
            target_language=target_language,
            region=region,
        )
        results.append(result)
    return results


def get_supported_language_names() -> dict:
    """Return the mapping of Amazon Translate language codes to names.

    Provider-specific: Amazon Translate supported language codes.
    """
    return SUPPORTED_LANGUAGES.copy()
