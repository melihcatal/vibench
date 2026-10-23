"""
Translate encryption or compliance notes for reviewers using Google Cloud Translation.
Google Cloud Translation (google-cloud-translate) is the concrete provider for translation.

This module translates cryptographic compliance notes into target languages
for international review teams using Google Cloud Translation API.
"""

import os
import json
from typing import List, Dict, Any, Optional

from google.cloud import translate_v2 as translate


# Google Cloud Translation client setup
# Authentication via GOOGLE_APPLICATION_CREDENTIALS environment variable
GOOGLE_TRANSLATION_MODEL = "nmt"  # Neural Machine Translation


def translate_compliance_note(
    text: str,
    target_language: str = "en",
    source_language: Optional[str] = None,
    format_type: str = "text",
) -> Dict[str, Any]:
    """
    Translate a compliance or encryption note using Google Cloud Translation.

    Uses Google Cloud Translation API v2 with the specified target language.

    Args:
        text: The compliance note text to translate.
        target_language: Target language code (e.g., 'en', 'de', 'ja').
        source_language: Source language code (auto-detect if None).
        format_type: Input format ('text' or 'html').

    Returns:
        Dict with translated text, detected source language, and metadata.

    Raises:
        ValueError: If text is empty.
        Exception: If Google Translation API call fails.
    """
    if not text:
        raise ValueError("text cannot be empty")

    # Initialize Google Cloud Translation client
    client = translate.Client()

    translate_kwargs = {
        "target_language": target_language,
        "format_": format_type,
    }

    if source_language:
        translate_kwargs["source_language"] = source_language

    result = client.translate(text, **translate_kwargs)

    translation_result = {
        "translated_text": result.get("translatedText", ""),
        "detected_source_language": result.get("detectedSourceLanguage", ""),
        "target_language": target_language,
        "input_length": len(text),
        "provider": "Google Cloud Translation",
    }

    return translation_result


def translate_compliance_notes_batch(
    notes: List[str],
    target_language: str = "en",
    source_language: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """
    Translate multiple compliance notes using Google Cloud Translation.

    Args:
        notes: List of compliance note strings.
        target_language: Target language code.
        source_language: Source language code (auto-detect if None).

    Returns:
        List of translation results.
    """
    results = []
    for i, note in enumerate(notes):
        try:
            result = translate_compliance_note(
                text=note,
                target_language=target_language,
                source_language=source_language,
            )
            result["note_index"] = i
            results.append(result)
        except Exception as e:
            results.append({
                "note_index": i,
                "error": str(e),
                "target_language": target_language,
            })
    return results


def translate_to_multiple_languages(
    text: str,
    target_languages: List[str],
    source_language: Optional[str] = None,
) -> Dict[str, Dict[str, Any]]:
    """
    Translate a compliance note to multiple target languages.

    Args:
        text: The text to translate.
        target_languages: List of target language codes.
        source_language: Source language code.

    Returns:
        Dict mapping language codes to translation results.
    """
    results = {}
    for lang in target_languages:
        result = translate_compliance_note(
            text=text,
            target_language=lang,
            source_language=source_language,
        )
        results[lang] = result
    return results


def format_compliance_note_for_translation(
    key_id: str,
    operation: str,
    status: str,
    details: str,
    reviewer_notes: str = "",
) -> str:
    """
    Format a compliance note for translation.

    Args:
        key_id: The encryption key ID.
        operation: The cryptographic operation performed.
        status: Operation status (success/failed).
        details: Additional details.
        reviewer_notes: Optional reviewer notes.

    Returns:
        Formatted compliance note string.
    """
    note_parts = [
        f"Key ID: {key_id}",
        f"Operation: {operation}",
        f"Status: {status}",
        f"Details: {details}",
    ]
    if reviewer_notes:
        note_parts.append(f"Reviewer Notes: {reviewer_notes}")
    return " | ".join(note_parts)


def main():
    """CLI entry point for compliance_note_translate."""
    text = os.environ.get(
        "COMPLIANCE_NOTE",
        "Encryption key rotation completed successfully for key-abc123. All encrypted payloads re-encrypted with new key version."
    )
    target_language = os.environ.get("TARGET_LANGUAGE", "de")
    source_language = os.environ.get("SOURCE_LANGUAGE") or None

    try:
        result = translate_compliance_note(
            text=text,
            target_language=target_language,
            source_language=source_language,
        )
        print("Compliance Note Translation (Google Cloud Translation):")
        print(f"Original: {text}")
        print(f"Translated: {result['translated_text']}")
        print(f"Detected Source: {result['detected_source_language']}")
        print(f"Target Language: {result['target_language']}")
    except Exception as e:
        print(f"Translation failed: {e}")
        exit(1)


if __name__ == "__main__":
    main()
