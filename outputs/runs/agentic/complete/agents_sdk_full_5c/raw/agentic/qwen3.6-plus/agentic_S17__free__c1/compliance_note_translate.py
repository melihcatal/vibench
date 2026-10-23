"""
compliance_note_translate.py - Translates encryption or compliance notes for reviewers using Amazon Translate.

Uses Amazon Translate (translate.us-east-1.amazonaws.com) to translate encryption
compliance notes, audit findings, and regulatory documentation between languages
for international security review teams.

Provider: Amazon Translate (translate.us-east-1.amazonaws.com)
Service: AWS Translate API via boto3
"""

import json
import logging
import sys
from typing import Dict, Optional

import boto3
from botocore.config import Config
from botocore.exceptions import ClientError

from security_models import ComplianceTranslation

logger = logging.getLogger(__name__)

REGION = "us-east-1"
DEFAULT_TARGET_LANGUAGE = "en"
DEFAULT_SOURCE_LANGUAGE = "auto"

SUPPORTED_LANGUAGES = {
    "en": "English",
    "es": "Spanish",
    "fr": "French",
    "de": "German",
    "ja": "Japanese",
    "zh": "Chinese (Simplified)",
    "zh-TW": "Chinese (Traditional)",
    "ko": "Korean",
    "ar": "Arabic",
    "pt": "Portuguese",
    "ru": "Russian",
    "it": "Italian",
    "nl": "Dutch",
    "hi": "Hindi",
    "tr": "Turkish",
    "pl": "Polish",
    "sv": "Swedish",
    "da": "Danish",
    "no": "Norwegian",
    "fi": "Finnish",
}


def get_translate_client(region: str = REGION) -> boto3.client:
    """
    Initialize an Amazon Translate client via boto3.
    Endpoint: translate.us-east-1.amazonaws.com
    """
    config = Config(
        retries={"max_attempts": 3, "mode": "adaptive"},
        region_name=region,
    )
    return boto3.client("translate", config=config)


def translate_text(
    text: str,
    target_language: str = DEFAULT_TARGET_LANGUAGE,
    source_language: str = DEFAULT_SOURCE_LANGUAGE,
    region: str = REGION,
) -> Dict:
    """
    Translate text using Amazon Translate API.

    Args:
        text: The source text to translate.
        target_language: Target language code (e.g., 'en', 'es', 'fr').
        source_language: Source language code. Use 'auto' for auto-detection.
        region: AWS region for Amazon Translate.

    Returns:
        Dict with translated text, source language, and confidence score.

    Raises:
        RuntimeError: If Amazon Translate fails.
    """
    client = get_translate_client(region)

    translate_kwargs = {
        "Text": text,
        "TargetLanguageCode": target_language,
    }

    if source_language != "auto":
        translate_kwargs["SourceLanguageCode"] = source_language
    else:
        translate_kwargs["SourceLanguageCode"] = "auto"

    try:
        response = client.translate_text(**translate_kwargs)
        return {
            "translated_text": response.get("TranslatedText", ""),
            "source_language": response.get("SourceLanguageCode", source_language),
            "target_language": target_language,
        }
    except ClientError as e:
        raise RuntimeError(
            f"Amazon Translate failed for target language {target_language}: {e}"
        ) from e


def translate_compliance_note(
    original_text: str,
    target_language: str = DEFAULT_TARGET_LANGUAGE,
    source_language: str = DEFAULT_SOURCE_LANGUAGE,
    region: str = REGION,
) -> ComplianceTranslation:
    """
    Translate an encryption or compliance note for international reviewers.

    Args:
        original_text: The original compliance/audit note text.
        target_language: Target language code for translation.
        source_language: Source language code. 'auto' for auto-detection.
        region: AWS region.

    Returns:
        ComplianceTranslation with original text, translated text, and metadata.

    Raises:
        RuntimeError: If translation fails.
    """
    result = translate_text(
        original_text,
        target_language=target_language,
        source_language=source_language,
        region=region,
    )

    translated_text = result["translated_text"]
    detected_source = result["source_language"]

    # Simple confidence heuristic based on text length preservation
    if len(original_text) > 0 and len(translated_text) > 0:
        ratio = min(len(translated_text), len(original_text)) / max(len(translated_text), len(original_text))
        confidence = round(min(1.0, ratio), 3)
    else:
        confidence = 0.0

    translation = ComplianceTranslation(
        original_text=original_text,
        translated_text=translated_text,
        source_language=detected_source,
        target_language=target_language,
        model="amazon-translate-v2",
        confidence=confidence,
    )

    source_name = SUPPORTED_LANGUAGES.get(detected_source, detected_source)
    target_name = SUPPORTED_LANGUAGES.get(target_language, target_language)

    logger.info(
        "Translated compliance note: %s -> %s (confidence: %.3f)",
        source_name,
        target_name,
        confidence,
    )
    return translation


def batch_translate_compliance_notes(
    notes: list,
    target_language: str = DEFAULT_TARGET_LANGUAGE,
    source_language: str = DEFAULT_SOURCE_LANGUAGE,
    region: str = REGION,
) -> list:
    """
    Translate multiple compliance notes in batch.

    Args:
        notes: List of compliance note strings.
        target_language: Target language code.
        source_language: Source language code or 'auto'.
        region: AWS region.

    Returns:
        List of ComplianceTranslation objects.
    """
    results = []
    for note in notes:
        translation = translate_compliance_note(
            note,
            target_language=target_language,
            source_language=source_language,
            region=region,
        )
        results.append(translation)
    return results


def main():
    """CLI entry point for compliance_note_translate."""
    if len(sys.argv) < 2:
        print("Usage: python compliance_note_translate.py <compliance_note> [target_language] [source_language]")
        sys.exit(1)

    original_text = sys.argv[1]
    target_lang = sys.argv[2] if len(sys.argv) > 2 else DEFAULT_TARGET_LANGUAGE
    source_lang = sys.argv[3] if len(sys.argv) > 3 else DEFAULT_SOURCE_LANGUAGE

    logging.basicConfig(level=logging.INFO)
    result = translate_compliance_note(
        original_text,
        target_language=target_lang,
        source_language=source_lang,
    )

    output = {
        "original_text": result.original_text,
        "translated_text": result.translated_text,
        "source_language": result.source_language,
        "target_language": result.target_language,
        "model": result.model,
        "confidence": result.confidence,
    }
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
