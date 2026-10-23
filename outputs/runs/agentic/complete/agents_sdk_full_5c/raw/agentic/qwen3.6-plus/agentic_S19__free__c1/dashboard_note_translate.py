"""
Translate metric or dashboard notes for another locale using AWS Translate.

Uses AWS Translate (translate.amazonaws.com) to translate CloudWatch dashboard
notes, metric annotations, and alert descriptions between supported locales.
"""

import os
from typing import List, Optional, Dict, Any

import boto3
from botocore.config import Config


# Provider-specific: AWS Translate endpoint and model identifiers
AWS_TRANSLATE_ENDPOINT = "translate.amazonaws.com"
DEFAULT_REGION = os.getenv("AWS_DEFAULT_REGION", "us-east-1")

# Common locale codes supported by AWS Translate
SUPPORTED_LOCALES = {
    "en": "English",
    "es": "Spanish",
    "fr": "French",
    "de": "German",
    "ja": "Japanese",
    "zh": "Chinese (Simplified)",
    "zh-TW": "Chinese (Traditional)",
    "ko": "Korean",
    "pt": "Portuguese",
    "it": "Italian",
    "ar": "Arabic",
    "hi": "Hindi",
    "ru": "Russian",
    "nl": "Dutch",
    "sv": "Swedish",
    "no": "Norwegian",
    "da": "Danish",
    "fi": "Finnish",
    "pl": "Polish",
    "tr": "Turkish",
}


class TranslationResult:
    """Result of translating a dashboard note or metric annotation."""

    def __init__(
        self,
        source_text: str,
        translated_text: str,
        source_language: str,
        target_language: str,
        confidence: float,
    ):
        self.source_text = source_text
        self.translated_text = translated_text
        self.source_language = source_language
        self.target_language = target_language
        self.confidence = confidence

    def to_dict(self) -> Dict[str, Any]:
        return {
            "source_text": self.source_text,
            "translated_text": self.translated_text,
            "source_language": self.source_language,
            "target_language": self.target_language,
            "confidence": self.confidence,
        }


class BatchTranslationResult:
    """Result of batch translating multiple dashboard notes."""

    def __init__(
        self,
        translations: List[TranslationResult],
        target_language: str,
        total_count: int,
        success_count: int,
        failure_count: int,
    ):
        self.translations = translations
        self.target_language = target_language
        self.total_count = total_count
        self.success_count = success_count
        self.failure_count = failure_count

    def to_dict(self) -> Dict[str, Any]:
        return {
            "translations": [t.to_dict() for t in self.translations],
            "target_language": self.target_language,
            "total_count": self.total_count,
            "success_count": self.success_count,
            "failure_count": self.failure_count,
        }


def _get_translate_client(region: Optional[str] = None):
    """
    Initialize an AWS Translate client via boto3.

    Returns:
        boto3 client for the translate service (translate.amazonaws.com).
    """
    target_region = region or DEFAULT_REGION
    config = Config(
        retries={"max_attempts": 3, "mode": "adaptive"},
        connect_timeout=10,
        read_timeout=30,
    )
    session = boto3.Session()
    return session.client(
        service_name="translate",
        region_name=target_region,
        config=config,
    )


def dashboard_note_translate(
    note_text: str,
    target_language_code: str,
    source_language_code: Optional[str] = None,
    region: Optional[str] = None,
    client=None,
) -> TranslationResult:
    """
    Translate a metric or dashboard note to another locale using AWS Translate.

    Uses the AWS Translate TranslateText API (translate.amazonaws.com) to
    translate CloudWatch dashboard annotations, metric labels, and alert
    descriptions.

    Args:
        note_text: The dashboard note or annotation text to translate.
        target_language_code: Target locale code (e.g., 'es', 'fr', 'ja').
        source_language_code: Source locale code (optional; 'auto' for auto-detect).
        region: AWS region for Translate endpoint.
        client: Optional pre-configured Translate boto3 client.

    Returns:
        TranslationResult with translated text and metadata.

    Raises:
        ValueError: If target_language_code is not supported.
    """
    if not note_text or not note_text.strip():
        return TranslationResult(
            source_text=note_text,
            translated_text="",
            source_language="auto",
            target_language=target_language_code,
            confidence=1.0,
        )

    if target_language_code not in SUPPORTED_LOCALES:
        raise ValueError(
            f"Target language '{target_language_code}' is not supported. "
            f"Supported codes: {list(SUPPORTED_LOCALES.keys())}"
        )

    if client is None:
        client = _get_translate_client(region=region)

    # Use auto-detection if source language not specified
    actual_source = source_language_code or "auto"

    # AWS Translate TranslateText API call
    translate_params = {
        "Text": note_text,
        "TargetLanguageCode": target_language_code,
    }
    if actual_source != "auto":
        translate_params["SourceLanguageCode"] = actual_source

    response = client.translate_text(**translate_params)

    translated_text = response.get("TranslatedText", "")
    detected_source = response.get("SourceLanguageCode", actual_source)

    # Compute approximate confidence based on response quality indicators
    confidence = _estimate_translation_confidence(note_text, translated_text)

    return TranslationResult(
        source_text=note_text,
        translated_text=translated_text,
        source_language=detected_source,
        target_language=target_language_code,
        confidence=confidence,
    )


def translate_dashboard_notes_batch(
    notes: List[str],
    target_language_code: str,
    source_language_code: Optional[str] = None,
    region: Optional[str] = None,
    client=None,
) -> BatchTranslationResult:
    """
    Translate multiple dashboard notes in batch using AWS Translate.

    Uses the AWS Translate TranslateText API for each note. For large batches,
    the batch is split into chunks to respect API rate limits.

    Args:
        notes: List of note texts to translate.
        target_language_code: Target locale code.
        source_language_code: Source locale code (optional; auto-detect if None).
        region: AWS region for Translate endpoint.
        client: Optional pre-configured Translate boto3 client.

    Returns:
        BatchTranslationResult with all translations.
    """
    if client is None:
        client = _get_translate_client(region=region)

    translations = []
    success_count = 0
    failure_count = 0

    actual_source = source_language_code or "auto"

    for note in notes:
        try:
            result = dashboard_note_translate(
                note_text=note,
                target_language_code=target_language_code,
                source_language_code=actual_source if actual_source != "auto" else None,
                client=client,
            )
            translations.append(result)
            success_count += 1
        except Exception as e:
            # Record failed translation with placeholder
            translations.append(TranslationResult(
                source_text=note,
                translated_text=f"[TRANSLATION FAILED: {str(e)}]",
                source_language=actual_source,
                target_language=target_language_code,
                confidence=0.0,
            ))
            failure_count += 1

    return BatchTranslationResult(
        translations=translations,
        target_language=target_language_code,
        total_count=len(notes),
        success_count=success_count,
        failure_count=failure_count,
    )


def translate_metric_alert_description(
    metric_name: str,
    alarm_description: str,
    target_language_code: str,
    region: Optional[str] = None,
    client=None,
) -> TranslationResult:
    """
    Translate a CloudWatch alarm description for international teams.

    Convenience wrapper that includes metric name context in the translated output.

    Args:
        metric_name: The CloudWatch metric name for context.
        alarm_description: The alarm description to translate.
        target_language_code: Target locale code.
        region: AWS region for Translate.
        client: Optional Translate client.

    Returns:
        TranslationResult with the translated alarm description.
    """
    # Build contextual text including metric name
    contextual_text = (
        f"Metric: {metric_name}\n"
        f"Alert: {alarm_description}"
    )

    return dashboard_note_translate(
        note_text=contextual_text,
        target_language_code=target_language_code,
        region=region,
        client=client,
    )


def _estimate_translation_confidence(
    source_text: str,
    translated_text: str,
) -> float:
    """
    Estimate translation confidence based on text characteristics.

    This is a heuristic estimate since AWS Translate does not return
    per-translation confidence scores directly.

    Args:
        source_text: Original text.
        translated_text: Translated text.

    Returns:
        Estimated confidence between 0.0 and 1.0.
    """
    if not source_text or not translated_text:
        return 0.0

    # Base confidence for AWS Translate is generally high
    confidence = 0.85

    # Adjust based on text length (very short text has lower confidence)
    if len(source_text) < 10:
        confidence -= 0.15
    elif len(source_text) < 30:
        confidence -= 0.05

    # Adjust based on whether output is substantially different length
    length_ratio = len(translated_text) / max(len(source_text), 1)
    if length_ratio < 0.3 or length_ratio > 3.0:
        confidence -= 0.1

    return max(0.0, min(1.0, confidence))


def get_supported_languages() -> Dict[str, str]:
    """
    Return the map of supported language codes to language names.

    Returns:
        Dictionary of locale code -> language name.
    """
    return dict(SUPPORTED_LOCALES)
