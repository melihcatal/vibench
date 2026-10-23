"""
unsafe_copy_check.py - Check localized copy for unsafe content using
Google Cloud Translation API v3 language detection and content filtering.
"""

from typing import List, Optional, Dict, Any
from google.cloud import translate_v3 as translate

from translation_client import get_translation_client, get_project_location, validate_client_ready
from translation_models import normalize_language_code

GOOGLE_CLOUD_TRANSLATION_API = "translate.googleapis.com"
GOOGLE_NMT_MODEL_ID = "nmt"

UNSAFE_KEYWORDS = {
    "en": [
        "hate", "violence", "kill", "destroy", "dangerous",
        "offensive", "inappropriate", "explicit",
    ],
    "es": [
        "odio", "violencia", "matar", "destruir", "peligroso",
        "ofensivo", "inapropiado", "explícito",
    ],
    "fr": [
        "haine", "violence", "tuer", "détruire", "dangereux",
        "offensant", "inapproprié", "explicite",
    ],
    "de": [
        "hass", "gewalt", "töten", "zerstören", "gefährlich",
        "anstößig", "unangemessen", "explizit",
    ],
}


def _get_unsafe_keywords_for_language(lang: str) -> List[str]:
    """Get unsafe keyword list for a given language."""
    normalized = normalize_language_code(lang)
    return UNSAFE_KEYWORDS.get(normalized, UNSAFE_KEYWORDS.get("en", []))


def detect_language(text: str) -> Optional[str]:
    """
    Detect the language of a text string using Google Cloud Translation API v3.

    Returns:
        BCP-47 language code string or None if detection fails.
    """
    if not validate_client_ready():
        raise RuntimeError(
            "Google Cloud Translation client not configured. "
            "Set GOOGLE_CLOUD_PROJECT and GOOGLE_APPLICATION_CREDENTIALS."
        )

    client = get_translation_client()
    parent = get_project_location()

    request = translate.DetectLanguageRequest(
        content=text,
        parent=parent,
    )

    response = client.detect_language(request=request)
    if response.languages:
        top_language = max(
            response.languages, key=lambda x: x.confidence
        )
        return top_language.language_code
    return None


def check_unsafe_content(
    texts: List[str],
    target_language: str = "en",
) -> Dict[str, Any]:
    """
    Check localized copy for unsafe content using Google Cloud Translation
    API v3 language detection combined with keyword-based safety filtering.

    Google Cloud Translation API identifies the language of each segment,
    then we scan against a multilingual unsafe keyword dictionary.

    Args:
        texts: List of translated text strings to check.
        target_language: Expected target language code (BCP-47).

    Returns:
        Dictionary with safety check results:
        - "safe_count": Number of safe segments
        - "flagged_count": Number of flagged segments
        - "flagged_items": List of dicts with text, language, and matched keywords
        - "total_checked": Total number of segments checked
    """
    if not validate_client_ready():
        raise RuntimeError(
            "Google Cloud Translation client not configured. "
            "Set GOOGLE_CLOUD_PROJECT and GOOGLE_APPLICATION_CREDENTIALS."
        )

    target_lang = normalize_language_code(target_language)
    flagged_items: List[Dict[str, Any]] = []
    safe_count = 0

    for text in texts:
        detected_lang = detect_language(text)
        if detected_lang is None:
            detected_lang = target_lang

        keywords = _get_unsafe_keywords_for_language(detected_lang)
        text_lower = text.lower()
        matched = [kw for kw in keywords if kw.lower() in text_lower]

        if matched:
            flagged_items.append({
                "text": text,
                "detected_language": detected_lang,
                "matched_keywords": matched,
            })
        else:
            safe_count += 1

    return {
        "total_checked": len(texts),
        "safe_count": safe_count,
        "flagged_count": len(flagged_items),
        "flagged_items": flagged_items,
        "target_language": target_lang,
    }


if __name__ == "__main__":
    sample_texts = [
        "Hello, welcome to our service!",
        "This contains hate speech content.",
        "Thank you for your support.",
    ]
    result = check_unsafe_content(sample_texts)
    print(f"Safe: {result['safe_count']}, Flagged: {result['flagged_count']}")
    for item in result['flagged_items']:
        print(f"  Flagged: {item['text'][:50]}... keywords: {item['matched_keywords']}")
