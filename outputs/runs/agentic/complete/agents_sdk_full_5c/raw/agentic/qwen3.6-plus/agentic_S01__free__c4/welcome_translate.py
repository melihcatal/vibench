"""
Translate onboarding copy into the user's locale.

Uses Google Cloud Translation API to translate welcome/onboarding
text into the target locale specified by the user's profile.
Provider: Google Cloud Translation (google.cloud.translate_v2).
"""

import os
from typing import Dict, List, Optional

from google.cloud import translate_v2 as translate


# Default onboarding copy in English (source locale)
DEFAULT_ONBOARDING_COPY: Dict[str, str] = {
    "welcome_title": "Welcome to Your New Account!",
    "welcome_body": "We're excited to have you on board. Let's get your profile set up so you can make the most of our platform.",
    "next_steps": "Complete your profile, explore the dashboard, and connect with your team.",
    "support_message": "Need help? Our support team is available 24/7.",
}


def _get_translation_client() -> translate.Client:
    """
    Build and return a Google Cloud Translation API client.
    Uses GOOGLE_APPLICATION_CREDENTIALS environment variable
    or the default service account from the runtime environment.

    Provider: Google Cloud Translation API (translate.googleapis.com)
    """
    return translate.Client()


def welcome_translate(
    target_locale: str,
    copy_override: Optional[Dict[str, str]] = None,
) -> Dict[str, str]:
    """
    Translate the full set of onboarding copy strings into the
    target locale using Google Cloud Translation.

    Provider: Google Cloud Translation v2 API.
    The google.cloud.translate_v2 import and translate.googleapis.com
    endpoint identify this as a Google Cloud-specific integration.

    Args:
        target_locale: BCP-47 language code (e.g., 'es', 'ja', 'fr').
        copy_override: Optional dict to override default onboarding copy.

    Returns:
        Dict mapping copy keys to translated strings in target_locale.
    """
    client = _get_translation_client()
    source_texts = copy_override or DEFAULT_ONBOARDING_COPY

    # Build list of (key, text) pairs for translation
    items = [(key, text) for key, text in source_texts.items() if text]
    if not items:
        return {}

    # Extract just the text values for batch translation
    texts = [text for _, text in items]

    # Google Cloud Translation batch translate call
    results = client.translate(
        texts,
        target_language=target_locale,
        source_language="en",
    )

    # Handle both single-result and batch-result responses
    translated: List[str] = []
    if isinstance(results, dict):
        translated = [results.get("translatedText", "")]
    else:
        translated = [r.get("translatedText", "") if isinstance(r, dict) else r for r in results]

    # Reconstruct the dict with translated values
    translated_copy: Dict[str, str] = {}
    for idx, (key, _) in enumerate(items):
        translated_copy[key] = translated[idx]

    return translated_copy


def translate_single_text(
    text: str,
    target_locale: str,
    source_locale: str = "en",
) -> str:
    """
    Translate a single string using Google Cloud Translation.

    Args:
        text: Source text to translate.
        target_locale: Target BCP-47 language code.
        source_locale: Source BCP-47 language code (default 'en').

    Returns:
        Translated string in target_locale.
    """
    client = _get_translation_client()
    result = client.translate(text, target_language=target_locale, source_language=source_locale)
    return result.get("translatedText", text) if isinstance(result, dict) else result
