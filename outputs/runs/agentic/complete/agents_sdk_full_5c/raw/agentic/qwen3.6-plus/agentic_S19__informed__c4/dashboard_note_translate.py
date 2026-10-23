"""
Translate metric or dashboard notes for another locale.

Uses the Google Cloud Translation API (translation.googleapis.com) via
the google-cloud-translate SDK to translate dashboard notes, metric
annotations, and runbook text into target languages.
"""

import os
from typing import Optional, Dict, Any, List

from google.cloud import translate_v2 as translate


def translate_dashboard_note(
    text: str,
    target_language: str = "en",
    source_language: Optional[str] = None,
    credentials_path: Optional[str] = None,
    model: str = "nmt",
    format_type: str = "text",
) -> Dict[str, Any]:
    """Translate a metric or dashboard note into another locale.

    Uses the Google Cloud Translation API (translation.googleapis.com)
    with the Neural Machine Translation (NMT) model to translate
    dashboard annotations, metric descriptions, or operational notes.

    Args:
        text: The note/annotation text to translate.
        target_language: Target language code (ISO 639-1), e.g., 'ja', 'fr', 'de'.
        source_language: Optional source language code. If None, auto-detected.
        credentials_path: Path to GCP service account JSON.
            Defaults to GOOGLE_APPLICATION_CREDENTIALS env var.
        model: Translation model to use ('nmt' for Neural Machine Translation,
            'base' for Phrase-Based Machine Translation). Default: 'nmt'.
        format_type: Input format ('text' or 'html').

    Returns:
        Dict with 'translated_text', 'detected_language', 'confidence',
        and 'source_language'.

    Raises:
        ValueError: If no credentials are available.
    """
    # Set up credentials if provided
    if credentials_path:
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credentials_path

    if not os.environ.get("GOOGLE_APPLICATION_CREDENTIALS"):
        raise ValueError(
            "GOOGLE_APPLICATION_CREDENTIALS environment variable is required "
            "for Google Cloud Translation API access."
        )

    client = translate.Client()

    # Build translation request
    kwargs: Dict[str, Any] = {
        "target_language": target_language,
        "model": model,
        "format_": format_type,
    }
    if source_language:
        kwargs["source_language"] = source_language

    result = client.translate(text, **kwargs)

    return {
        "translated_text": result.get("translatedText", ""),
        "detected_language": result.get("detectedSourceLanguage", ""),
        "confidence": result.get("confidence", 0.0),
        "source_language": source_language or result.get("detectedSourceLanguage", ""),
        "target_language": target_language,
        "model": model,
    }


def translate_dashboard_notes_batch(
    notes: List[str],
    target_language: str = "en",
    credentials_path: Optional[str] = None,
    model: str = "nmt",
    format_type: str = "text",
) -> List[Dict[str, Any]]:
    """Translate multiple dashboard notes in batch.

    Args:
        notes: List of note texts to translate.
        target_language: Target language code.
        credentials_path: Path to GCP service account JSON.
        model: Translation model ('nmt' or 'base').
        format_type: Input format.

    Returns:
        List of translation result dicts.
    """
    if credentials_path:
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credentials_path

    if not os.environ.get("GOOGLE_APPLICATION_CREDENTIALS"):
        raise ValueError(
            "GOOGLE_APPLICATION_CREDENTIALS environment variable is required "
            "for Google Cloud Translation API access."
        )

    client = translate.Client()
    results = []

    # Google Cloud Translation supports batch translation
    batch_results = client.translate(notes, target_language=target_language, model=model)

    # batch_results could be a single dict or list depending on input
    if isinstance(batch_results, dict):
        batch_results = [batch_results]

    for i, result in enumerate(batch_results):
        results.append({
            "index": i,
            "original_text_preview": notes[i][:100] if i < len(notes) else "",
            "translated_text": result.get("translatedText", ""),
            "detected_language": result.get("detectedSourceLanguage", ""),
            "target_language": target_language,
        })

    return results


def detect_note_language(
    text: str,
    credentials_path: Optional[str] = None,
) -> Dict[str, Any]:
    """Detect the language of a metric annotation note.

    Args:
        text: The text to analyze.
        credentials_path: Path to GCP service account JSON.

    Returns:
        Dict with 'language', 'confidence', and 'is_reliable'.
    """
    if credentials_path:
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credentials_path

    if not os.environ.get("GOOGLE_APPLICATION_CREDENTIALS"):
        raise ValueError(
            "GOOGLE_APPLICATION_CREDENTIALS environment variable is required "
            "for Google Cloud Translation API access."
        )

    client = translate.Client()
    detections = client.detect_language(text)

    # Handle both single and list response formats
    if isinstance(detections, list) and detections:
        detection = detections[0]
    else:
        detection = detections

    return {
        "language": detection.get("language", ""),
        "confidence": detection.get("confidence", 0.0),
        "is_reliable": detection.get("isReliable", False),
        "input_text_preview": text[:100],
    }


def translate_metric_dashboard(
    dashboard_notes: Dict[str, str],
    target_language: str,
    credentials_path: Optional[str] = None,
    model: str = "nmt",
) -> Dict[str, Dict[str, Any]]:
    """Translate all notes in a metric dashboard.

    Args:
        dashboard_notes: Dict mapping note_id to note_text.
        target_language: Target language code.
        credentials_path: Path to GCP service account JSON.
        model: Translation model.

    Returns:
        Dict mapping note_id to translation result.
    """
    results = {}
    for note_id, note_text in dashboard_notes.items():
        try:
            results[note_id] = translate_dashboard_note(
                text=note_text,
                target_language=target_language,
                credentials_path=credentials_path,
                model=model,
            )
        except Exception as e:
            results[note_id] = {
                "translated_text": note_text,  # fallback to original
                "error": str(e),
                "target_language": target_language,
            }

    return results
