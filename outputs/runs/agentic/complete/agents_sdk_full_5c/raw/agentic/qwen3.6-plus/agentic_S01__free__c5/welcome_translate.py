"""
Translate onboarding copy into the user's locale using the Google Cloud Translation API v2.
Uses the google-cloud-translate Python SDK to call the hosted Google Cloud Translation
service for translating welcome/onboarding text.
"""

import os
from typing import Dict, List
from google.cloud import translate_v2 as translate_v2


GOOGLE_CLOUD_PROJECT = os.getenv("GOOGLE_CLOUD_PROJECT", "")
GOOGLE_APPLICATION_CREDENTIALS = os.getenv("GOOGLE_APPLICATION_CREDENTIALS", "")

DEFAULT_ONBOARDING_COPY: Dict[str, str] = {
    "welcome_title": "Welcome to our platform!",
    "welcome_body": "We're excited to have you on board. Let's get started with setting up your profile.",
    "next_steps": "Next, verify your email address and complete your profile setup.",
    "support_link": "Need help? Contact our support team anytime.",
}


def get_translate_client() -> translate_v2.Client:
    """Create a Google Cloud Translate v2 client using application default credentials."""
    return translate_v2.Client()


def translate_onboarding_copy(
    target_language: str,
    copy_map: Dict[str, str] | None = None,
) -> Dict[str, str]:
    """
    Translate onboarding copy into the user's target locale using Google Cloud Translation.

    Args:
        target_language: ISO 639-1 language code (e.g., 'es', 'fr', 'ja').
        copy_map: Optional dict of copy keys to English source text.
                  Defaults to DEFAULT_ONBOARDING_COPY.

    Returns:
        Dict with the same keys and translated values.
    """
    source_texts = copy_map or DEFAULT_ONBOARDING_COPY
    texts = list(source_texts.values())

    if target_language == "en":
        return dict(source_texts)

    client = get_translate_client()

    results = client.translate(
        texts,
        target_language=target_language,
        source_language="en",
    )

    translated = {}
    keys = list(source_texts.keys())
    for i, key in enumerate(keys):
        if isinstance(results, list):
            translated[key] = results[i]["translatedText"]
        else:
            translated[key] = results["translatedText"]

    return translated


def translate_single_text(text: str, target_language: str) -> str:
    """
    Translate a single string using Google Cloud Translation API v2.

    Args:
        text: Source text in English.
        target_language: ISO 639-1 language code.

    Returns:
        Translated text string.
    """
    if target_language == "en":
        return text

    client = get_translate_client()
    result = client.translate(text, target_language=target_language, source_language="en")
    return result["translatedText"]


if __name__ == "__main__":
    translated = translate_onboarding_copy(target_language="es")
    for key, value in translated.items():
        print(f"{key}: {value}")
