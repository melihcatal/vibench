"""
Translate metric or dashboard notes for another locale.

Uses Amazon Translate API to translate dashboard notes and metric annotations
into target languages.

Provider signals:
  - boto3 translate client (Amazon Translate)
  - Amazon Translate service endpoint
  - AWS Translate API (translate_text)
"""

from typing import Any, Dict, List, Optional

import boto3
from botocore.config import Config

from observability_client import AWS_REGION


SOURCE_LANGUAGE_CODE = "auto"
TARGET_LANGUAGE_CODE = "en"


def _create_translate_client():
    """Create a boto3 Amazon Translate client."""
    config = Config(
        retries={"max_attempts": 3, "mode": "standard"},
    )
    session = boto3.Session(region_name=AWS_REGION)
    return session.client("translate", config=config)


class TranslationResult:
    """Result of translating a dashboard note."""

    def __init__(
        self,
        original_text: str,
        translated_text: str,
        source_language: str,
        target_language: str,
    ):
        self.original_text = original_text
        self.translated_text = translated_text
        self.source_language = source_language
        self.target_language = target_language

    def to_dict(self) -> Dict[str, Any]:
        return {
            "original_text": self.original_text,
            "translated_text": self.translated_text,
            "source_language": self.source_language,
            "target_language": self.target_language,
        }


def dashboard_note_translate(
    note_text: str,
    target_language_code: str = TARGET_LANGUAGE_CODE,
    source_language_code: str = SOURCE_LANGUAGE_CODE,
) -> TranslationResult:
    """
    Translate a metric or dashboard note into another locale.

    Uses Amazon Translate to translate CloudWatch dashboard annotations,
    metric labels, and alert notes for internationalized dashboards.

    Args:
        note_text: The original dashboard note or metric annotation text
        target_language_code: Target language code (e.g., 'es', 'fr', 'de', 'ja', 'zh')
        source_language_code: Source language code (default: 'auto' for auto-detect)

    Returns:
        TranslationResult with original and translated text.
    """
    translate = _create_translate_client()

    if source_language_code == "auto":
        source_lang = _detect_language(note_text, translate)
    else:
        source_lang = source_language_code

    truncated = note_text[:10000] if len(note_text) > 10000 else note_text

    response = translate.translate_text(
        Text=truncated,
        SourceLanguageCode=source_lang,
        TargetLanguageCode=target_language_code,
    )

    translated = response.get("TranslatedText", "")
    detected_source = response.get("SourceLanguageCode", source_lang)

    return TranslationResult(
        original_text=note_text,
        translated_text=translated,
        source_language=detected_source,
        target_language=target_language_code,
    )


def _detect_language(text: str, translate_client) -> str:
    """Detect language of text using Amazon Translate's built-in detection."""
    try:
        truncated = text[:10000] if len(text) > 10000 else text
        response = translate_client.translate_text(
            Text=truncated,
            SourceLanguageCode="auto",
            TargetLanguageCode="en",
        )
        return response.get("SourceLanguageCode", "en")
    except Exception:
        return "en"


def translate_dashboard_notes(
    notes: List[Dict[str, str]],
    target_language_code: str = TARGET_LANGUAGE_CODE,
) -> List[TranslationResult]:
    """
    Translate a batch of dashboard notes.

    Args:
        notes: List of dicts with 'note_id' and 'text' keys
        target_language_code: Target language code

    Returns:
        List of TranslationResult objects.
    """
    results = []
    for note in notes:
        text = note.get("text", "")
        if text:
            translation = dashboard_note_translate(text, target_language_code)
            results.append(translation)
    return results


def translate_metric_annotation(
    metric_name: str,
    annotation_text: str,
    namespace: str,
    target_language_code: str = "ja",
) -> Dict[str, Any]:
    """
    Translate a CloudWatch metric annotation for a specific locale.

    Args:
        metric_name: CloudWatch metric name
        annotation_text: Original annotation text
        namespace: CloudWatch namespace
        target_language_code: Target language code

    Returns:
        Dict with translation metadata.
    """
    result = dashboard_note_translate(annotation_text, target_language_code)

    return {
        "metric_name": metric_name,
        "namespace": namespace,
        "original_language": result.source_language,
        "target_language": result.target_language,
        "original_text": result.original_text,
        "translated_text": result.translated_text,
    }
