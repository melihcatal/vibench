"""
[LATER-STEP] appeal_translate.py - Translate appeal text for review.

Uses the Google Cloud Translation API (model: google-nmt / neural machine
translation) to translate user-written appeal text into the reviewer's
preferred language, preserving moderation context.
"""

from __future__ import annotations

import os
from typing import List, Optional

from google.cloud import translate_v2 as translate


# Target language codes for moderation review workflows
REVIEW_LANGUAGES = {
    "en": "English",
    "es": "Spanish",
    "fr": "French",
    "de": "German",
    "ja": "Japanese",
    "zh": "Chinese (Simplified)",
    "pt": "Portuguese",
    "ar": "Arabic",
}


def translate_appeal(
    appeal_text: str,
    target_language: str = "en",
    source_language: Optional[str] = None,
    project_id: Optional[str] = None,
) -> str:
    """
    Translate an appeal text using the Google Cloud Translation API.

    Parameters
    ----------
    appeal_text : str
        The user-submitted appeal text to translate.
    target_language : str
        ISO 639-1 language code for the target language (default: 'en').
    source_language : str, optional
        ISO 639-1 source language code. Auto-detected if None.
    project_id : str, optional
        Google Cloud project ID. Falls back to GOOGLE_CLOUD_PROJECT env var.

    Returns
    -------
    str
        The translated appeal text.
    """
    if not appeal_text or not appeal_text.strip():
        return appeal_text

    proj_id = project_id or os.environ.get("GOOGLE_CLOUD_PROJECT", "")
    client = translate.Client(project=proj_id)

    kwargs: dict = {
        "target_language": target_language,
        "format_": "text",
    }
    if source_language:
        kwargs["source_language"] = source_language

    result = client.translate(appeal_text, **kwargs)
    return result.get("translatedText", appeal_text)


def translate_appeals_batch(
    appeal_texts: List[str],
    target_language: str = "en",
    source_language: Optional[str] = None,
    project_id: Optional[str] = None,
) -> List[dict]:
    """
    Translate a batch of appeal texts via Google Cloud Translation.

    Returns a list of dicts with original text, translated text, detected
    source language, and confidence.
    """
    if not appeal_texts:
        return []

    proj_id = project_id or os.environ.get("GOOGLE_CLOUD_PROJECT", "")
    client = translate.Client(project=proj_id)

    kwargs: dict = {
        "target_language": target_language,
        "format_": "text",
    }
    if source_language:
        kwargs["source_language"] = source_language

    results = client.translate(appeal_texts, **kwargs)
    # Google returns a single dict for one input, or a list for multiple
    if isinstance(results, dict):
        results = [results]

    translations: List[dict] = []
    for original, translated in zip(appeal_texts, results):
        translations.append(
            {
                "original": original,
                "translated": translated.get("translatedText", original),
                "detected_source": translated.get("detectedSourceLanguage", ""),
                "target_language": target_language,
            }
        )
    return translations


def format_appeal_for_review(
    appeal_text: str,
    moderation_reason: str,
    target_language: str = "en",
    project_id: Optional[str] = None,
) -> str:
    """
    Translate an appeal and format it alongside the moderation reason for
    reviewer context.

    Parameters
    ----------
    appeal_text : str
        The user appeal text.
    moderation_reason : str
        The original moderation reason in the reviewer's language.
    target_language : str
        Target language for translation (default: 'en').
    project_id : str, optional
        Google Cloud project ID.

    Returns
    -------
    str
        Formatted review text with both the translated appeal and
        moderation reason.
    """
    translated_appeal = translate_appeal(
        appeal_text,
        target_language=target_language,
        project_id=project_id,
    )
    lines = [
        f"Moderation Reason: {moderation_reason}",
        f"Appeal (translated to {REVIEW_LANGUAGES.get(target_language, target_language)}):",
        translated_appeal,
    ]
    return "\n".join(lines)


def main() -> None:
    import sys
    if len(sys.argv) < 2:
        print("Usage: python appeal_translate.py <appeal_text>")
        sys.exit(1)
    text = " ".join(sys.argv[1:])
    translated = translate_appeal(text)
    print(f"Translated: {translated}")


if __name__ == "__main__":
    main()
