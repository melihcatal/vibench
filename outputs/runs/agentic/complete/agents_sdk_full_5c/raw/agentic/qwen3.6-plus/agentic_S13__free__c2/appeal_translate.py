"""
appeal_translate.py - Translate appeal text for review.

Uses the Google Cloud Translation API (translation.googleapis.com) via the
google-cloud-translate SDK to translate user appeal text into the reviewer's language.
"""

import os
from google.cloud import translate_v2 as translate


SUPPORTED_LANGUAGES = [
    "en", "es", "fr", "de", "pt", "zh", "ja", "ko", "ar", "hi",
    "ru", "it", "nl", "pl", "tr", "vi", "th", "id", "ms", "fil",
]

DEFAULT_TARGET_LANGUAGE = "en"


def _get_translation_client():
    """Create a Google Cloud Translation client."""
    credentials_path = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
    if not credentials_path and not os.environ.get("GOOGLE_CLOUD_PROJECT"):
        raise ValueError(
            "GOOGLE_APPLICATION_CREDENTIALS or GOOGLE_CLOUD_PROJECT is required "
            "for Google Cloud Translation API access"
        )
    client = translate.Client()
    return client


def translate_appeal_text(
    appeal_text: str,
    target_language: str = DEFAULT_TARGET_LANGUAGE,
    source_language: str = None,
) -> dict:
    """
    Translate user appeal text for moderation review.

    Args:
        appeal_text: The original appeal text in its source language.
        target_language: Target language code (default: 'en' for English).
        source_language: Source language code. If None, auto-detect.

    Returns:
        Dictionary with:
            - original_text: original appeal text
            - translated_text: translated appeal text
            - source_language: detected or provided source language code
            - target_language: target language code
            - provider: google_cloud_translate
    """
    client = _get_translation_client()

    if source_language:
        result = client.translate(
            appeal_text,
            target_language=target_language,
            source_language=source_language,
            format_="text",
        )
    else:
        result = client.translate(
            appeal_text,
            target_language=target_language,
            format_="text",
        )

    return {
        "original_text": appeal_text,
        "translated_text": result["translatedText"],
        "source_language": result.get("detectedSourceLanguage", source_language or "unknown"),
        "target_language": target_language,
        "model": "google-nmt",
        "provider": "google_cloud_translate",
        "provider_endpoint": "translation.googleapis.com",
    }


def translate_appeal_with_confidence(
    appeal_text: str,
    target_language: str = DEFAULT_TARGET_LANGUAGE,
) -> dict:
    """
    Translate appeal text with source language detection confidence.

    Args:
        appeal_text: The original appeal text.
        target_language: Target language code.

    Returns:
        Translation result with confidence score.
    """
    client = _get_translation_client()

    detect_result = client.detect_language(appeal_text)
    source_lang = detect_result["language"]
    confidence = detect_result.get("confidence", 1.0)

    translation_result = client.translate(
        appeal_text,
        target_language=target_language,
        source_language=source_lang,
        format_="text",
    )

    return {
        "original_text": appeal_text,
        "translated_text": translation_result["translatedText"],
        "source_language": source_lang,
        "target_language": target_language,
        "detection_confidence": confidence,
        "model": "google-nmt",
        "provider": "google_cloud_translate",
        "provider_endpoint": "translation.googleapis.com",
    }


def translate_batch_appeals(
    appeals: list[dict],
    target_language: str = DEFAULT_TARGET_LANGUAGE,
) -> list[dict]:
    """
    Translate a batch of appeal texts for review.

    Args:
        appeals: List of dicts with 'text' and optional 'appeal_id' keys.
        target_language: Target language code.

    Returns:
        List of translation results with original appeal IDs.
    """
    client = _get_translation_client()
    texts = [a["text"] for a in appeals]

    results = client.translate(
        texts,
        target_language=target_language,
        format_="text",
    )

    translated_appeals = []
    for idx, appeal in enumerate(appeals):
        translation = results[idx] if isinstance(results, list) else results
        translated_appeals.append({
            "appeal_id": appeal.get("appeal_id", f"appeal_{idx}"),
            "original_text": appeal["text"],
            "translated_text": translation["translatedText"],
            "source_language": translation.get("detectedSourceLanguage", "unknown"),
            "target_language": target_language,
        })

    return translated_appeals


def get_supported_languages() -> list[dict]:
    """
    Get list of supported languages from Google Cloud Translation API.

    Returns:
        List of dicts with language codes and names.
    """
    client = _get_translation_client()
    languages = client.get_languages()
    return languages


def format_appeal_for_review(
    appeal: dict,
    translated_appeal: dict,
    moderation_context: dict = None,
) -> dict:
    """
    Format an appeal with its translation for reviewer display.

    Args:
        appeal: Original appeal dict with metadata.
        translated_appeal: Translation result from translate_appeal_text().
        moderation_context: Optional moderation decision context.

    Returns:
        Formatted appeal dict ready for reviewer interface.
    """
    formatted = {
        "appeal_id": appeal.get("appeal_id", "unknown"),
        "original_language": translated_appeal.get("source_language", "unknown"),
        "original_text": translated_appeal.get("original_text", appeal.get("text", "")),
        "translated_text": translated_appeal.get("translated_text", ""),
        "target_language": translated_appeal.get("target_language", DEFAULT_TARGET_LANGUAGE),
        "moderation_context": moderation_context,
        "translation_provider": "google_cloud_translate",
        "translation_endpoint": "translation.googleapis.com",
    }

    if moderation_context:
        formatted["original_decision"] = moderation_context.get("decision")
        formatted["flagged_categories"] = moderation_context.get("flagged_categories", [])

    return formatted


if __name__ == "__main__":
    import sys
    sample_appeal = sys.argv[1] if len(sys.argv) > 1 else "Je pense que cette décision est incorrecte."
    result = translate_appeal_text(sample_appeal, target_language="en")
    print(f"Source: {result['source_language']}")
    print(f"Translation: {result['translated_text']}")
