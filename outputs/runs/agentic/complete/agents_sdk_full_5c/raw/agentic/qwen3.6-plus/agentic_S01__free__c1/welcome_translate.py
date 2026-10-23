"""
Translate onboarding copy into the user's locale using Google Cloud Translation API.
Provider: Google Cloud Translation API (google-cloud-translate)
"""

import os
from typing import Dict, Any, Optional, List

from google.cloud import translate_v2 as translate
from google.api_core.exceptions import GoogleAPIError


GOOGLE_TRANSLATE_MODEL_ID = "nmt"  # Neural Machine Translation model
DEFAULT_ONBOARDING_COPY = {
    "en": {
        "welcome_title": "Welcome to our platform!",
        "welcome_subtitle": "Let's get you set up in just a few steps.",
        "profile_setup": "Complete your profile",
        "email_verification": "Verify your email address",
        "terms_accept": "Accept terms and conditions",
        "get_started": "Get Started",
    }
}


def get_welcome_copy(
    locale: str,
    source_locale: str = "en",
    project_id: Optional[str] = None,
    custom_copy: Optional[Dict[str, str]] = None,
) -> Dict[str, Any]:
    """
    Translate onboarding welcome copy into the user's locale.

    Args:
        locale: Target locale code (e.g., 'es', 'fr', 'de', 'ja')
        source_locale: Source locale code (default: 'en')
        project_id: Google Cloud project ID
        custom_copy: Optional dict of custom strings to translate

    Returns:
        Dict with translated copy strings
    """
    project = project_id or os.environ.get("GOOGLE_CLOUD_PROJECT", "")
    if not project:
        return _fallback_copy(locale, custom_copy)

    copy_to_translate = custom_copy or DEFAULT_ONBOARDING_COPY.get(source_locale, {})
    if not copy_to_translate:
        return _fallback_copy(locale, custom_copy)

    texts = list(copy_to_translate.values())

    try:
        client = translate.Client(project=project)
        result = client.translate(
            texts,
            target_language=locale,
            source_language=source_locale,
            model=GOOGLE_TRANSLATE_MODEL_ID,
            format_="text",
        )

        translated_texts = []
        if isinstance(result, list):
            for item in result:
                translated_texts.append(item.get("translatedText", item.get("input", "")))
        else:
            translated_texts = [result.get("translatedText", "")]

        translated_copy = {}
        for key, translated_text in zip(copy_to_translate.keys(), translated_texts):
            translated_copy[key] = translated_text

        return {
            "locale": locale,
            "source_locale": source_locale,
            "copy": translated_copy,
            "model": GOOGLE_TRANSLATE_MODEL_ID,
            "provider": "google_cloud_translation",
            "success": True,
        }

    except GoogleAPIError as exc:
        return {
            "locale": locale,
            "source_locale": source_locale,
            "copy": _fallback_copy(locale, custom_copy),
            "model": GOOGLE_TRANSLATE_MODEL_ID,
            "provider": "google_cloud_translation",
            "success": False,
            "error": str(exc),
        }


def translate_single_string(
    text: str,
    target_locale: str,
    source_locale: str = "en",
    project_id: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Translate a single string into the target locale.

    Args:
        text: The text to translate
        target_locale: Target locale code
        source_locale: Source locale code
        project_id: Google Cloud project ID

    Returns:
        Dict with translation result
    """
    project = project_id or os.environ.get("GOOGLE_CLOUD_PROJECT", "")
    if not project:
        return {
            "original": text,
            "translated": text,
            "target_locale": target_locale,
            "provider": "google_cloud_translation",
            "success": False,
            "error": "Google Cloud project not configured",
        }

    try:
        client = translate.Client(project=project)
        result = client.translate(
            text,
            target_language=target_locale,
            source_language=source_locale,
            model=GOOGLE_TRANSLATE_MODEL_ID,
        )

        return {
            "original": text,
            "translated": result.get("translatedText", text),
            "target_locale": target_locale,
            "source_locale": source_locale,
            "model": GOOGLE_TRANSLATE_MODEL_ID,
            "provider": "google_cloud_translation",
            "success": True,
        }

    except GoogleAPIError as exc:
        return {
            "original": text,
            "translated": text,
            "target_locale": target_locale,
            "provider": "google_cloud_translation",
            "success": False,
            "error": str(exc),
        }


def _fallback_copy(locale: str, custom_copy: Optional[Dict[str, str]] = None) -> Dict[str, str]:
    """Return fallback copy when translation is unavailable."""
    return custom_copy or DEFAULT_ONBOARDING_COPY.get("en", {})


if __name__ == "__main__":
    import sys

    locale = sys.argv[1] if len(sys.argv) > 1 else "es"
    result = get_welcome_copy(locale=locale)
    print(f"Translated copy for {locale}:")
    for key, value in result.get("copy", {}).items():
        print(f"  {key}: {value}")
